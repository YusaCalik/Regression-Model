select *from data$

alter table [data$]
add Month_Number int;

UPDATE data$  
SET Month_Number =case Month
					when 'January' then 1
					when 'February' then 2
					when 'March' then 3
					when 'April' then 4
					when 'May' then 5
					when 'June' then 6
					when 'July' then 7
					when 'August' then 8
					when 'September' then 9
					when 'October' then 10
					when 'November' then 11
					when 'December' then 12
				end ;

select * from data$

--T3 Table doesnt have PreviousMonth Payment Value..
select State_id,Year,Month_Number,
SUM(payment_installments) Total_Installment,sum(product_description_lenght) Total_Product_Description,sum(product_name_lenght) Total_Product_Name_Length,
AVG(product_photos_qty) Photos_Quality,SUM(payment_value) Total_Payment,LAG(sum(payment_value)) OVER(order by Year,Month_Number) as PreviousMonthPayment,
LAG(sum(payment_value),3) OVER(order by Year,Month_Number) as SeasonalPayment,LAG(sum(payment_value),4) OVER(order by Year,Month_Number) as QuarterPayment,
LAG(sum(payment_value),12) OVER(order by Year,Month_Number) as LastYearPayment
into ttl
from [data$]
group by State_id,Year,Month_Number;
							
select * from ttl
where State_id=22
order by Year,Month_Number


ALTER TABLE dbo.ttl
   ADD CONSTRAINT FK_Customer_State_dataframe$ FOREIGN KEY (State_id)
      REFERENCES dbo.[Customer_State_dataframe$] (State_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
;
