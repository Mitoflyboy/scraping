!function(a){"use strict";function b(a){function b(){e={},e[g]=function(){m.measureAndSend(h,void 0,g)},e[i]=function(){m.clearMarks(),m.clearMeasures(),l=!0,m.mark(j)}}function c(b,c,d){function e(){var a,b,e;return a=c?c:"navigationStart",b=d?d:"now",e=[a,",",b].join("")}var f,g;f=m.getEntriesByName(b,"measure"),"object"==typeof f&&f.length>0&&(g=f[f.length-1].duration,a.edap=a.edap||[],b===h?a.edap.push(function(a){a.trigger("primary.action.rendered",{eventtime:""+g,initialpageload:""+!l})}):a.edap.push(function(a){a.trigger("generic.timing",{eventcategory:"performance timing",eventname:e(),eventtime:""+g})}))}function d(a){e||b(),"function"==typeof e[a]&&e[a]()}var e,f,g="primary.action.rendered",h="primary.action.loadtime",i="page.unload",j="spa.navigation.start",k=["navigationStart","unloadEventStart","unloadEventEnd","redirectStart","redirectEnd","fetchStart","domainLookupStart","domainLookupEnd","connectStart","connectEnd","secureConnectionStart","requestStart","responseStart","responseEnd","domLoading","domInteractive","domContentLoadedEventStart","domContentLoadedEventEnd","domComplete","loadEventStart","loadEventEnd"],l=!1,m=this;return a=a||window||{},f=a.performance,a.edap=a.edap||[],f?(a.addEventListener("load",function(){function b(){var b,c,d,e,f=m.timing,g={};if(b=f.navigationStart){for(e=0;e<k.length;e++)c=k[e],d=f[c]-b,d>=0&&(g[c.toLowerCase()]=""+d);a.edap.push(function(a){a.trigger("performance.timing",g)})}}setTimeout(b,0)}),this.timing=f.timing||{},this.measure=function(a,b,c){var d;return!b&&l&&(b=j),b||(b="navigationStart"),d=[a,b],c&&d.push(c),f.measure.apply(f,d)},this.measureAndSend=function(a,b,d){var e;return!b&&l&&(b=j),e=m.measure.apply(f,arguments),c(a,b,d),e},this.clearMarks=function(){return f.clearMarks.apply(f,arguments)},this.clearMeasures=function(){return f.clearMeasures.apply(f,arguments)},this.getEntriesByType=function(){return f.getEntriesByType.apply(f,arguments)},this.getEntriesByName=function(){return f.getEntriesByName.apply(f,arguments)},void(this.mark=function(a){var b;return b=f.mark.apply(f,arguments),d(a),b})):void a.edap.push(function(a){a.error(new TypeError("Missing window.performance, polyfill failed to load"))})}a.ha=a.ha||{},function(a){"undefined"==typeof a&&(a={}),"undefined"==typeof a.performance&&(a.performance={}),a._perfRefForUserTimingPolyfill=a.performance,a.performance.userTimingJsNow=!1,a.performance.userTimingJsNowPrefixed=!1,a.performance.userTimingJsUserTiming=!1,a.performance.userTimingJsUserTimingPrefixed=!1,a.performance.userTimingJsPerformanceTimeline=!1,a.performance.userTimingJsPerformanceTimelinePrefixed=!1;var b,c,d=[],e=[],f=null;if("function"!=typeof a.performance.now){for(a.performance.userTimingJsNow=!0,e=["webkitNow","msNow","mozNow"],b=0;b<e.length;b++)if("function"==typeof a.performance[e[b]]){a.performance.now=a.performance[e[b]],a.performance.userTimingJsNowPrefixed=!0;break}var g=+new Date;a.performance.timing&&a.performance.timing.navigationStart?g=a.performance.timing.navigationStart:"undefined"!=typeof process&&"function"==typeof process.hrtime&&(g=process.hrtime(),a.performance.now=function(){var a=process.hrtime(g);return 1e3*a[0]+1e-6*a[1]}),"function"!=typeof a.performance.now&&(Date.now?a.performance.now=function(){return Date.now()-g}:a.performance.now=function(){return+new Date-g})}var h=function(){},i=function(){},j=[],k=!1,l=!1;if("function"!=typeof a.performance.getEntries||"function"!=typeof a.performance.mark){for("function"==typeof a.performance.getEntries&&"function"!=typeof a.performance.mark&&(l=!0),a.performance.userTimingJsPerformanceTimeline=!0,d=["webkit","moz"],e=["getEntries","getEntriesByName","getEntriesByType"],b=0;b<e.length;b++)for(c=0;c<d.length;c++)f=d[c]+e[b].substr(0,1).toUpperCase()+e[b].substr(1),"function"==typeof a.performance[f]&&(a.performance[e[b]]=a.performance[f],a.performance.userTimingJsPerformanceTimelinePrefixed=!0);h=function(a){j.push(a),"measure"===a.entryType&&(k=!0)};var m=function(){k&&(j.sort(function(a,b){return a.startTime-b.startTime}),k=!1)};if(i=function(a,c){for(b=0;b<j.length;)j[b].entryType===a&&("undefined"==typeof c||j[b].name===c)?j.splice(b,1):b++},"function"!=typeof a.performance.getEntries||l){var n=a.performance.getEntries;a.performance.getEntries=function(){m();var b=j.slice(0);return l&&n&&(Array.prototype.push.apply(b,n.call(a.performance)),b.sort(function(a,b){return a.startTime-b.startTime})),b}}if("function"!=typeof a.performance.getEntriesByType||l){var o=a.performance.getEntriesByType;a.performance.getEntriesByType=function(c){if("undefined"==typeof c||"mark"!==c&&"measure"!==c)return l&&o?o.call(a.performance,c):[];"measure"===c&&m();var d=[];for(b=0;b<j.length;b++)j[b].entryType===c&&d.push(j[b]);return d}}if("function"!=typeof a.performance.getEntriesByName||l){var p=a.performance.getEntriesByName;a.performance.getEntriesByName=function(c,d){if(d&&"mark"!==d&&"measure"!==d)return l&&p?p.call(a.performance,c,d):[];"undefined"!=typeof d&&"measure"===d&&m();var e=[];for(b=0;b<j.length;b++)("undefined"==typeof d||j[b].entryType===d)&&j[b].name===c&&e.push(j[b]);return l&&p&&(Array.prototype.push.apply(e,p.call(a.performance,c,d)),e.sort(function(a,b){return a.startTime-b.startTime})),e}}}if("function"!=typeof a.performance.mark){for(a.performance.userTimingJsUserTiming=!0,d=["webkit","moz","ms"],e=["mark","measure","clearMarks","clearMeasures"],b=0;b<e.length;b++)for(c=0;c<d.length;c++)f=d[c]+e[b].substr(0,1).toUpperCase()+e[b].substr(1),"function"==typeof a.performance[f]&&(a.performance[e[b]]=a.performance[f],a.performance.userTimingJsUserTimingPrefixed=!0);var q={};"function"!=typeof a.performance.mark&&(a.performance.mark=function(b){var c=a.performance.now();if("undefined"==typeof b)throw new SyntaxError("Mark name must be specified");if(a.performance.timing&&b in a.performance.timing)throw new SyntaxError("Mark name is not allowed");q[b]||(q[b]=[]),q[b].push(c),h({entryType:"mark",name:b,startTime:c,duration:0})}),"function"!=typeof a.performance.clearMarks&&(a.performance.clearMarks=function(a){a?q[a]=[]:q={},i("mark",a)}),"function"!=typeof a.performance.measure&&(a.performance.measure=function(b,c,d){var e=a.performance.now();if("undefined"==typeof b)throw new SyntaxError("Measure must be specified");if(!c)return void h({entryType:"measure",name:b,startTime:0,duration:e});var f=0;if(a.performance.timing&&c in a.performance.timing){if("navigationStart"!==c&&0===a.performance.timing[c])throw new Error(c+" has a timing of 0");f=a.performance.timing[c]-a.performance.timing.navigationStart}else{if(!(c in q))throw new Error(c+" mark not found");f=q[c][q[c].length-1]}var g=e;if(d)if(g=0,a.performance.timing&&d in a.performance.timing){if("navigationStart"!==d&&0===a.performance.timing[d])throw new Error(d+" has a timing of 0");g=a.performance.timing[d]-a.performance.timing.navigationStart}else{if(!(d in q))throw new Error(d+" mark not found");g=q[d][q[d].length-1]}var i=g-f;h({entryType:"measure",name:b,startTime:f,duration:i})}),"function"!=typeof a.performance.clearMeasures&&(a.performance.clearMeasures=function(a){i("measure",a)})}"function"==typeof define&&define.amd?define([],function(){return a.performance}):"undefined"!=typeof module&&"undefined"!=typeof module.exports&&(module.exports=a.performance)}("undefined"!=typeof window?window:void 0);var c=new b(a);c.mark("analytics.polyfill.loaded"),a.ha.userTiming=c}(window);