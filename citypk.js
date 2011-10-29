(function($){

// SHOW/HIDE LOADING
function loading(){
	$('#loading').spin({
		lines: 15,
		length: 10,
		width: 2,
		radius: 20,
		color: '#000',
		speed: 1.1,
		trail: 50,
		shadow: false
	});
}

// ===================================================================================================
// MODEL : BATTLE
window.BATTLE = Backbone.Model.extend({
	url: '/api/battle/',
	initialize: function() {
		this.fetch();

		// LOAD BATTLE PLAYERS
		_.each(this.get('fighters'),function(f){
		
			if ()
			{
			
			}
		
		});
		
	},
	s: function() {
		
	}
});


// ===================================================================================================
// MODEL : CITY
window.CITY = Backbone.Model.extend({
	initialize: function() {

	},
	s: function() {
		
	}
});

// ===================================================================================================



// ===================================================================================================
// CLASS : ROUTER

window.CITYPK = Backbone.Router.extend({
	routes: {
		'battle/:id':		'battle'
	},
	initialize: function(){
		window.user = new User();
		loading();
	},
	battle: function(id){
	
		// CREATE BATTLE MODEL
		window.battle = new BATTLE({
			"id": id
		});
		
	
	}
});

$(function(){
	window.App = new MTFM();
	Backbone.history.start();
});


})(jQuery);