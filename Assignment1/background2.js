
var callback = function(req) {
    console.log("REQ", req);

var FILTERS = [
 
    "/googlead-",
    "/googlead.",
    "/googlead1.",
    "/googlead160.",
    "/GoogleAd300.",
    "/googlead336x280.",
    "/googlead_",
    "/GoogleAdBg.",
    "/googleadcode.",
    "/googleaddfooter.",
    "/googleaddisplayframe.",
    "/googleadhp.",
    "/googleadhpbot.",
    "/googleadhtml/*",
    "/googleadiframe_",
    "/googleadright.",
    "/googleads-",
    "/googleads.",
    "/googleads/*",
    "/googleads1.",
    "/googleads2.",
    "/googleads3widetext.",
    "/googleads_",
    "/googleadsafc_",
    "/googleadsafs_",
    "/googleAdScripts.",
    "/googleadsense.",
    "/googleAdTaggingSubSec.",
    "/googleadunit?",
    "/googleafc.",
    "/googleafs.",
    "/googleafvadrenderer.",
    "/googlecontextualads.",
    "/googleheadad.",
    "/googleleader.",
    "/googleleads.",
    "/p8network.js",
    "/page-ads.",
    "/page-peel",
    "/page/ad/*",
    "/pagead/ads?",
    "/pagead/conversion.",
    "/pagead/gen_",
    "/pagead/html/*",
    "/pagead/js/*",
    "/pagead/lvz?",
    "/pagead/osd.",
    "/pagead2.",
    "/pagead46.",
    "/pagead?",
    "/pageadimg/*",
    "/pageads/*",
    "/pagecall_dfp_async.",
    "/pagecurl/*",
    "/pageear.",
    "/pageear/*",
    "/pageear_",
    "/pagepeel-",
    "/pagepeel.",
    "/pagepeel/*",
    "/pagepeel_",
    "/pagepeelads.",
    "/pages/ads"

   ];

     for (var i=0; i != FILTERS.length; ++i) {
      var f = FILTERS[i];

      if (req.url.indexOf(f) !== -1) {

        console.warn("BLOCKED", req, "as", req.type, "with", f);
        return { cancel: true };
      }
    }

    return null;
  }


 var options = {
    urls: [
      "http://*/*",
      "https://*/*",
      // "https://www.learncbse.in/"
    ],
    types: ["image", "sub_frame"]
  };


chrome.webRequest.onBeforeRequest.addListener(callback,  options, ["blocking"]);
