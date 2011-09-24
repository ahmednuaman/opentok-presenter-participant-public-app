var S	= {
	apiKey														: '4901211',
	channel														: '',
	channelId													: '',
	resizeFunctions												: [ ],
	session														: '',
	sessionId													: '3b0c7ef2b12a4e194afb06000c2f6c75',
	streams														: [ ],
	tokenId														: 'devtoken',
	
	ready														: function()
	{
		$( 'html' ).removeClass( 'no-js' );
		
		if ( S.checkEventSource() && TB.checkSystemRequirements() === TB.HAS_REQUIREMENTS )
		{
			$( '#badbrowser' ).remove();
		}
		else
		{
			$( '#container' ).remove();
		}
		
		S.setupLoader();
		S.setupListener();
		
		$( window ).resize( S.windowResize ).resize();
		
		S.hideLoader();
	},
	
	windowResize												: function(e)
	{
		var win	= $( window );
		var h	= win.height();
		var w	= win.width();
		var l	= S.resizeFunctions.length;
		var f;
		
		for ( var i = 0; i < l; i++ )
		{
			f	= S.resizeFunctions[ i ];
			
			f( w, h );
		}
	},
	
	checkEventSource											: function()
	{
		return ( 'EventSource' in window );
	},
	
	setupLoader													: function()
	{
		S.resizeFunctions.push( S.repositionLoader );
	},
	
	repositionLoader											: function(w, h)
	{
		var l	= $( '#loader-inner' );
		
		l.css({
			top		: ( h - l.height() ) / 2,
			left	: ( w - l.width() ) / 2
		});
	},
	
	hideLoader													: function()
	{
		$( '#loader' ).stop( true ).fadeOut();
	},
	
	showLoader													: function()
	{
		$( '#loader' ).stop( true ).fadeOut();
	},
	
	setupListener												: function()
	{
		$.post( '/api', function(d)
		{
			S.channelId	= d;
			
			var channel	= new goog.appengine.Channel( S.channelId );
			
			S.channel	= channel.open();
			
			S.channel.onopen	= S.channelOpen;
			S.channel.onmessage	= S.channelMessage;
		});
	},
	
	channelOpen													: function(e)
	{
		console.log(e);
	},
	
	channelMessage												: function(e)
	{
		console.log(e);
	},
	
	setupSession												: function()
	{
		S.session	= TB.initSession( S.sessionId );
		
		S.session.addEventListener( 'sessionConnected', 	S.sessionConnectedHandler );
		S.session.addEventListener( 'sessionDisconnected', 	S.sessionDisconnectedHandler );
		S.session.addEventListener( 'connectionCreated', 	S.connectionCreatedHandler );
		S.session.addEventListener( 'connectionDestroyed', 	S.connectionDestroyedHandler );
		S.session.addEventListener( 'streamCreated', 		S.streamCreatedHandler );
		S.session.addEventListener( 'streamDestroyed', 		S.streamDestroyedHandler );
		
		S.session.connect( S.apiKey, S.tokenId );
	},
	
	sessionConnectedHandler										: function(e)
	{
		// for ( var i = 0; i < e.streams.length; i++ ) 
		// 		{
		// 			S.addStream( e.streams[ i ] );
		// 		}
		S.session.subscribe( e.streams[ S.streams[ 0 ] ], 'stream-presenter' );
		S.session.subscribe( e.streams[ S.streams[ 1 ] ], 'stream-participant' );
	},
	
	sessionDisconnectedHandler									: function(e)
	{
		
	},
	
	connectionCreatedHandler									: function(e)
	{
		
	},
	
	connectionDestroyedHandler									: function(e)
	{
		
	},
	
	streamCreatedHandler										: function(e)
	{
		
	},
	
	streamDestroyedHandler										: function(e)
	{
		
	}
};

$( document ).ready( S.ready );