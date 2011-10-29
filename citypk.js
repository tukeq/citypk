(function($){

// JQUERY SPIN - http://fgnass.github.com/spin.js
(function(a,b,c){function n(a){var b={x:a.offsetLeft,y:a.offsetTop};while(a=a.offsetParent)b.x+=a.offsetLeft,b.y+=a.offsetTop;return b}function m(a,b){for(var d in b)a[d]===c&&(a[d]=b[d]);return a}function l(a,b){for(var c in b)a.style[k(a,c)||c]=b[c];return a}function k(a,b){var e=a.style,f,g;if(e[b]!==c)return b;b=b.charAt(0).toUpperCase()+b.slice(1);for(g=0;g<d.length;g++){f=d[g]+b;if(e[f]!==c)return f}}function j(a,b){var c=["opacity",b,~~(a*100)].join("-"),f="{opacity:"+a+"}",g,h;if(!e[c]){for(h=0;h<d.length;h++){g=d[h]&&"-"+d[h].toLowerCase()+"-"||"";try{i.insertRule("@"+g+"keyframes "+c+"{0%{opacity:1}"+b+"%"+f+"to"+f+"}",0),i.insertRule(".spin ."+c+"{"+g+"animation: "+c+" 1s linear infinite}",1)}catch(j){}}e[c]=1}return c}function h(a,b,c){c&&!c.parentNode&&h(a,c),a.insertBefore(b,c||null);return a}function g(a,c){var d=b.createElement(a||"div"),e;for(e in c)d[e]=c[e];return d}var d=["webkit","Moz","ms","O"],e={},f;h(b.getElementsByTagName("head")[0],g("style"));var i=b.styleSheets[b.styleSheets.length-1],o=function(a){this.opts=m(a||{},{lines:12,trail:100,length:7,width:5,radius:10,color:"#000",opacity:.25,speed:1})},p=o.prototype={spin:function(a){var b=this,c=b.el=l(g(),{position:"relative"}),d,e;a&&(e=n(h(a,c,a.firstChild)),d=n(c),l(c,{left:(a.offsetWidth>>1)-d.x+e.x+"px",top:(a.offsetHeight>>1)-d.y+e.y+"px"})),b.lines(c,b.opts),setTimeout(function(){c.className="spin"},1);if(!f){var i=b.opts,j=0,k=20/i.speed,m=(1-i.opacity)/(k*i.trail/100),o=k/i.lines;(function p(){j++;for(var a=i.lines;a;a--){var d=Math.max(1-(j+a*o)%k*m,i.opacity);b.opacity(c,i.lines-a,d,i)}b.timeout=b.el&&setTimeout(p,50)})()}return b},stop:function(){var a=this,b=a.el;clearTimeout(a.timeout),b&&b.parentNode&&b.parentNode.removeChild(b),a.el=c;return a}};p.lines=function(a,b){function f(a,c){return l(g(),{position:"absolute",width:b.length+b.width+"px",height:b.width+"px",background:a,boxShadow:c,transformOrigin:"left",transform:"rotate("+~~(360/b.lines*d)+"deg) translate("+b.radius+"px"+",0)",borderRadius:"100em"})}var c=j(b.opacity,b.trail),d=0,e;for(;d<b.lines;d++)e=l(g(0,{className:c}),{position:"absolute",top:1+~(b.width/2)+"px",transform:"translate3d(0,0,0)",opacity:b.opacity,animationDuration:1/b.speed+"s",animationDelay:~~(1e3/b.lines/b.speed*d)+"ms"}),b.shadow&&h(e,l(f("#000","0 0 4px #000"),{top:"2px"})),h(a,h(e,f(b.color,"0 0 1px rgba(0,0,0,.1)")));return a},p.opacity=function(a,b,c){a.childNodes[b].style.opacity=c},function(){var a=l(g("group"),{behavior:"url(#default#VML)"}),b;if(!k(a,"transform")&&a.adj){for(b=4;b--;)i.addRule(["group","roundrect","fill","stroke"][b],"behavior:url(#default#VML)");p.lines=function(a,b){function k(a,d,i){h(f,h(l(e(),{rotation:360/b.lines*a+"deg",left:~~d}),h(l(g("roundrect",{arcsize:1}),{width:c,height:b.width,left:b.radius,top:-b.width>>1,filter:i}),g("fill",{color:b.color,opacity:b.opacity}),g("stroke",{opacity:0}))))}function e(){return l(g("group",{coordsize:d+" "+d,coordorigin:-c+" "+ -c}),{width:d,height:d})}var c=b.length+b.width,d=2*c,f=e(),i=~(b.length+b.radius+b.width)+"px",j;if(b.shadow)for(j=1;j<=b.lines;j++)k(j,-2,"progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)");for(j=1;j<=b.lines;j++)k(j);return h(l(a,{margin:i+" 0 0 "+i}),f)},p.opacity=function(a,b,c,d){d=d.shadow&&d.lines||0,a.firstChild.childNodes[b+d].firstChild.firstChild.opacity=c}}else f=k(a,"animation")}(),a.Spinner=o})(window,document)
$.fn.spin = function(opts) {this.each(function() {var $this = $(this),spinner = $this.data('spinner');if (spinner) spinner.stop();if (opts !== false) {opts = $.extend({color: $this.css('color')}, opts);spinner = new Spinner(opts).spin(this);$this.data('spinner', spinner);}});return this;};


// ===================================================================================================
// MODEL : BATTLE
window.BATTLE = Backbone.Model.extend({
	initialize: function() {
		this.url = 'api/battle/'+this.id;
		this.fetch({
			success: function(r){
				//console.log(this.get('fighters'));
				
				// LOAD BATTLE PLAYERS
				_.each(this.get('fighters'),function(f){
				
					// SET FIGHTER ID
					var fid = (typeof window.fighter == 'undefined') ? 0 : 1 ;
					
					// UPDATE UI WITH FIGHTER INFO
					$('#fighter'+fid+'name').html(f.name); // NAME
					$('#fighter'+fid+'desc').html(f.description); // DESCRIPTION
					
					// CREATE FIGHTER POSTS MODEL
					window.fighter[fid] = new FIGHTER({
							posts: f.posts,
							city: fid,
							url: '/api/posts/'+window.bf_id+'/'+fid+'/'
					});
				
				});			
			},
			error: function(r){
				console.log('error');
				console.log(r);
				//alert('oh shit!');
			}
		});		
	}
});


// ===================================================================================================
// MODEL : FIGHTER POSTS
window.FIGHTER = Backbone.Model.extend({
	initialize: function() {
		var city = this.get('city');
		
		if (typeof window.posts[city] == 'undefined'){
			window.posts[city] = new POSTS({
				id: 'fighter'+city+'posts'
			});
		}
		
		this.bind('change',function(){
			window.posts[this.get('city')].render();
		});			
	},
	update: function() {
	

	
	}
});


// ===================================================================================================
// VIEW : POSTS


window.POSTS = Backbone.View.extend({
	tagName: 'div',
	events: {
		'click .refresh': 'refresh'
	},
	initialize: function(){
		this.render();
	},
	refresh: function(){
	
	}
});

// ===================================================================================================
// CLASS : ROUTER

window.CITYPK = Backbone.Router.extend({
	routes: {
		'battle/:id':		'battle'
	},
	initialize: function(){
		
		$('#loading').spin({
			lines: 10,
			length: 7,
			width: 4,
			radius: 10,
			color: '#000',
			speed: 1.1,
			trail: 50,
			shadow: false
		});
		
	},
	battle: function(id) {
		
		// SET BATTLEFIELD ID
		window.bf_id = id;
		
		// CREATE BATTLE MODEL
		window.battle = new BATTLE({
			id: bf_id
		});
		

		
	}
});

$(function(){
	window.App = new CITYPK();
	Backbone.history.start();
});


})(jQuery);