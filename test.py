import re

text = 'PAID Roll Express Anardana Chowk, Patiala SS: M: 96469-79620 From Swiggy[49890100388]) Name: SWIGGY SS Date; 26/08/19 Delivery mB 15:54 Cashier: gagan Bill No.: 16447 Token No.: 36 Item Qty. Price Amount Panéer Malai 2 85.00 170.00 Tikka Roll (Single) Tota! Qty: 2. Sub Total 170.00 SGST 2.5% 4.25 CGST 2.5% 4.25 Round off +0.50 Grand Total 179.00 Paid via Online [Swiggy] Thanks For Choosing Roll Express We Hope To See You Soon Again'
text = text.lower()
res = text.rfind('total')
text = text[res+6:]
res = text.find(' ')
text = text[0:res]
print(text)