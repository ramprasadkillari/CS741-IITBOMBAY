var callback = function(details) {

      var requestURL=details.url;
      console.log("Test");

      if(details.method == "GET") {
            var dec_URL=decodeURIComponent(requestURL);
            var splitURL=dec_URL.split("?data=");
            param=splitURL[1];
            
            param=param.replace(/\s/g, "");
            param=param.replace(/\+/g, "");
            
            if( param.match(/<script/gi) ||  param.match(/%3cscript/gi) || param.match(/javascript:/gi) || param.match(/on.*=/gi) ) return {cancel: true};   

      }  else if(details.method == "POST") {
    
            var mydata=details.requestBody.formData;
            var mypost=JSON.stringify(mydata.data );
            mypost=mypost.replace(/\s/g, "");
            mypost=mypost.replace(/\+/g, "");
            mypost=mypost.replace(/\\/g, "");
            console.log(mypost)
            if( mypost.match(/<script/gi) || mypost.match(/%3cscript/gi) || mypost.match(/javascript:/gi) || mypost.match(/on.*=/gi) ) return {cancel: true};

      }   
        
};

var filter={urls: ["<all_urls>"]};
var opt_extrainfo=["blocking", "requestBody"];

chrome.webRequest.onBeforeRequest.addListener(callback,filter,opt_extrainfo );
