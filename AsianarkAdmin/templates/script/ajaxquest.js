<script type="text/javascript">
var xmlhttp;
function createxmlhttprequest()
{
	if (window.XMLHttpRequest)
	  { 
	  xmlhttp=new XMLHttpRequest();
	  }
	else if (window.ActiveXObject)
	  { 
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  }
	return xmlhttp;
}
function sendRequest(url)
{
	 if(xmlhttp==null){
	     xmlhttp = createxmlhttprequest();
	 }
	 xmlhttp.onreadystatechange=sendResponse;
	 xmlhttp.open("GET",url,true);
	 xmlhttp.send(null);
}
function sendResponse()
{
   if (xmlhttp.readyState==4)
  { 
  if (xmlhttp.status==200)
    { 
		var dom=document.getElementById("xm_sidebar_right");
		dom.innerHTML=xmlhttp.responseText;
    }
  else
    {
    alert("Problem retrieving data:" + xmlhttp.statusText);
    }
  }
}

</script>