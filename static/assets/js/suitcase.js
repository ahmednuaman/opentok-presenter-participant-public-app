var S	= {
	resizeFunctions												: [ ],
	
	ready														: function()
	{
		$( 'html' ).removeClass( 'no-js' );
		
		if ( S.checkEventSource() )
		{
			$( '#badbrowser' ).remove();
		}
		else
		{
			$( '#container' ).remove();
		}
		
		S.setupLoader();
		
		$( window ).resize( S.windowResize ).resize();
		
		//S.hideLoader();
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
	}
};

$( document ).ready( S.ready );