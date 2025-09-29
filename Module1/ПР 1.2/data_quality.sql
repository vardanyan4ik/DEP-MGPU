--Проверка количества записей
-- Сравнение объема данных между слоями
SELECT 
    (SELECT COUNT(*) FROM stg.orders) as stg_orders_count,
    (SELECT COUNT(*) FROM dw.sales_fact) as dw_sales_count;



--Проверка целостности данных
sql
-- Проверка ссылочной целостности
SELECT COUNT(*) as broken_links
FROM dw.sales_fact f
LEFT JOIN dw.customer_dim c ON f.cust_id = c.cust_id
WHERE c.cust_id IS NULL;

-- Проверка на дубликаты
SELECT customer_id, COUNT(*)
FROM dw.customer_dim
GROUP BY customer_id
HAVING COUNT(*) > 1;


--Проверка корректности расчетов
-- Сверка контрольных сумм
SELECT 
    ROUND(SUM(sales), 2) as total_sales_stg,
    ROUND(SUM(profit), 2) as total_profit_stg
FROM stg.orders;

SELECT 
    ROUND(SUM(sales), 2) as total_sales_dw,
    ROUND(SUM(profit), 2) as total_profit_dw
FROM dw.sales_fact;