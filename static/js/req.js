function req(){
	var ip_adress = document.getElementById('ip').value;
	var date1 = document.getElementById('datetime1').value;
	var date2 = document.getElementById('datetime2').value;
	
	//alert('/circle/' + '\?ip='+ip_adress + 'datetime1='+date1+'&datetime2='+date2)
	document.getElementById("if1").src = '/circle/' + '\?ip='+ip_adress + '&datetime1='+date1+'&datetime2='+date2;
		document.getElementById("if2").src = '/line/' + '\?ip='+ip_adress + '&datetime1='+date1+'&datetime2='+date2;
		document.getElementById("if3").src = '/net_bar/' + '\?ip='+ip_adress + '&datetime1='+date1+'&datetime2='+date2;
		document.getElementById("if4").src = '/info_tab/' + '\?ip='+ip_adress + '&datetime1='+date1+'&datetime2='+date2;

	/*if (datet1 == '' && date2 == '' && ip_adress== ''){
		document.getElementById("if1").src = '/circle/';
		document.getElementById("if2").src = '/line/';
		document.getElementById("if3").src = '/net_bar/';
		document.getElementById("if4").src = '/info_tab/';
	}
	else if(){
		document.getElementById("if1").src = '/circle/' + ip_adress + '/\?datetime1='+date1+'&datetime2='+date2;
		document.getElementById("if2").src = '/line/' + ip_adress + '/\?datetime1='+date1+'&datetime2='+date2;
		document.getElementById("if3").src = '/net_bar/' + ip_adress + '/\?datetime1='+date1+'&datetime2='+date2;
		document.getElementById("if4").src = '/info_tab/' + ip_adress + '/\?datetime1='+date1+'&datetime2='+date2;
	}
	else{
		document.getElementById("if1").src = '/circle/' + ip_adress;
		document.getElementById("if2").src = '/line/' + ip_adress;
		document.getElementById("if3").src = '/net_bar/' + ip_adress;
		document.getElementById("if4").src = '/info_tab/' + ip_adress;
	}
{% endif %}	*/
}