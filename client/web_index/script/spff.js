//参考了CSDN上的代码
//作者：LeetCoder 
//来源：CSDN 
//原文：https://blog.csdn.net/baozhiqiangjava/article/details/80212965 

/**
 * 获取URL参数
 * @param 参数名
 * @returns 参数值
 */
function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]);
    return null;
}


function getContent(search_method,search_arg){
	//$("result1").empty();
	if (document.getElementById("result1")!=null) {
		document.getElementById("result1").innerHTML ="";
	}
	
	if (search_method==null || search_method.length<=0 || search_arg==null || search_arg.length <=0) {

		var url="http://spfftmp.campanula.wang/REQ_SEARCH_BY_TIME";
		var message = 'data={"limit_year_time":"2019"}';
	}
	else {
		var url="http://spfftmp.campanula.wang/" + search_method;
		var message = 'data={"limit_year_time":"' + search_arg + '"}';
	}
	$(function(){
		$.getJSON(url,message,function(data){
			parseContent(data);
		})
	});
}

function parseContent(data){
	//console.log(data);
	var rows = data.data.result_list;
	//console.log(rows);
	for (var i=0;i<rows.length;i++) {
		createDiv(rows[i]);
	}
}

function createDiv(data){
	var divString = '<a class="weui-cell weui-cell_access"' +
	 ' href="./spffDetail.html?id=' + data.case_id + '">          ' +
'                <div class="weui-cell__bd">                      ' +
'                    <p>' + data.title+ '</p>                     ' +
'                </div>                                           ' +
'                <div class="weui-cell__ft">                      ' + 
                     data.ctime + '</div>                         ' + 
'            </a>                                                 ';

	
	$div = $(divString);
	//$div.find('.h2').html("<a href='/spffDetail?id="+data.case_id+"'>"+ data.title + "</a>");
	
	$div.appendTo( $('div#result1') );
	//console.log('div inserted');
}


var search_method = GetQueryString("method");
var search_arg = GetQueryString("data");

if (search_method==null || search_method.length<=0 || search_arg==null || search_arg.length <=0) {
	getContent(null,null);

} else {
	getContent(search_method,search_arg);

}


