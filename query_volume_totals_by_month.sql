WITH TradeEntryVolumeData AS (
    SELECT DATEADD(MONTH, DATEDIFF(MONTH, 0, te.OrderAcceptedDateTime), 0) AcceptedMonth
        ,SUM(COALESCE(ted.Quantity, 0)) Quantity
        ,te.TradeEntryId
    FROM TradeEntryDetail ted WITH (NOLOCK)
    INNER JOIN TradeEntry te WITH (NOLOCK) ON  ted.TradeEntryId = te.TradeEntryId
    WHERE te.OrderStatusCvId = 1104
    GROUP BY te.TradeEntryId,  DATEADD(month, DATEDIFF(month, 0, te.OrderAcceptedDateTime),0) 

), MonthlyVolumes AS (
    SELECT tevd.AcceptedMonth
        ,SUM(tevd.Quantity) TotalAccepted
		,COUNT(DISTINCT tevd.TradeEntryId) TotalAcceptedTrades
    FROM TradeEntryVolumeData tevd WITH (NOLOCK)
    GROUP BY tevd.AcceptedMonth
), WithBusinessDasy AS (
	SELECT subquery.TotalBusinessDays
		  ,CASE WHEN subquery.ElapsedBusinessDays <= 0 THEN 1 ELSE subquery.ElapsedBusinessDays END ElapsedBusinessDays -- handles divide by 0 case
		  ,subquery.AcceptedMonth
		  ,subquery.TotalAccepted
		  ,subquery.TotalAcceptedTrades
	FROM 
	(
		 SELECT * 
			, (
				(DATEDIFF(dd, mv.AcceptedMonth, DATEADD(d, -1, DATEADD(m, DATEDIFF(m, 0, mv.AcceptedMonth) + 1, 0))) + 1)
				-(DATEDIFF(wk, mv.AcceptedMonth, (DATEADD(d, -1, DATEADD(m, DATEDIFF(m, 0, mv.AcceptedMonth) + 1, 0)))) * 2)
				-(CASE WHEN DATENAME(dw, mv.AcceptedMonth) = 'Sunday' THEN 1 ELSE 0 END)
				-(CASE WHEN DATENAME(dw, mv.AcceptedMonth) = 'Saturday' THEN 1 ELSE 0 END)
			) TotalBusinessDays
			, CASE 
				WHEN GETDATE() > (DATEADD(d, -1, DATEADD(m, DATEDIFF(m, 0, mv.AcceptedMonth) + 1, 0))) THEN NULL
				ELSE  (
					(DATEDIFF(dd, mv.AcceptedMonth, DATEADD(DAY, DATEDIFF(day, 0, GETDATE()),0)) + 1)
					-(DATEDIFF(wk, mv.AcceptedMonth, DATEADD(DAY, DATEDIFF(day, 0, GETDATE()),0)) * 2)
					-(CASE WHEN DATENAME(dw, mv.AcceptedMonth) = 'Sunday' THEN 1 ELSE 0 END)
					-(CASE WHEN DATENAME(dw, mv.AcceptedMonth) = 'Saturday' THEN 1 ELSE 0 END)
				)
			END ElapsedBusinessDays
		FROM MonthlyVolumes mv
	) subquery


), Projected AS (
    SELECT CONVERT(VARCHAR, AcceptedMonth, 101) Month
        ,TotalAccepted
		,TotalAcceptedTrades
        ,FORMAT(TotalAccepted, 'N') TotalAcceptedVolume
        ,WithBusinessDasy.TotalBusinessDays
        ,COALESCE(WithBusinessDasy.ElapsedBusinessDays, WithBusinessDasy.TotalBusinessDays) ElapsedBusinessDays
        ,WithBusinessDasy.AcceptedMonth
    FROM WithBusinessDasy WITH (NOLOCK)

)
SELECT Month
    ,TotalAcceptedVolume as Accepted
	,TotalAcceptedTrades
    ,CAST(FORMAT((TotalAccepted/ElapsedBusinessDays)*TotalBusinessDays, 'N') as VARCHAR(Max)) Projected
    ,'(' + CAST(ElapsedBusinessDays as VARCHAR(Max)) +'/' + CAST(TotalBusinessDays as VARCHAR(Max)) + ')' as  [Business Days]
FROM Projected WITH (NOLOCK)
WHERE Month >= DATEADD(MONTH, -12, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0))
ORDER BY Month