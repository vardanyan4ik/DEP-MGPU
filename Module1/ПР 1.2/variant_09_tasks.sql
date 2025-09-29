-- Задание 1: Создать представление по скидкам
--Логика:
--JOIN между stg.orders и dw.product_dim по product_id
--Группировка по category
--Расчет средней скидки в % и общей суммы предоставленных скидок

Создание VIEW для повторного использования
CREATE OR REPLACE VIEW dw.discounts_view AS
SELECT 
    p.category,
    ROUND(AVG(o.discount) * 100, 2) AS average_discount_percent,
    SUM(o.sales * o.discount) AS total_discount_amount
FROM stg.orders o
JOIN dw.product_dim p ON o.product_id = p.product_id
GROUP BY p.category;

-- Задание 2: Посчитать общее количество проданных товаров в разрезе категорий

Логика:
--Простая агрегация из stg.orders
--Группировка по category

SUM(quantity) для получения общего количества
SELECT 
    category,
    SUM(quantity) AS total_quantity
FROM stg.orders
GROUP BY category;

-- Задание 3: Проанализировать эффективность работы менеджеров по регионам

Логика:
--JOIN stg.orders с people по region (менеджер закреплен за регионом)
--Группировка по person (менеджеру)
--Расчет общей прибыли, средней прибыли на заказ и количества заказов
--Сортировка по убыванию прибыли для выявления лучших менеджеров

SELECT 
    p.person AS manager,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(AVG(o.profit), 2) AS average_profit_per_order,
    COUNT(DISTINCT o.order_id) AS orders_count
FROM stg.orders o
JOIN people p ON o.region = p.region  -- без указания схемы, ищет в public или текущей
GROUP BY p.person
ORDER BY total_profit DESC;

