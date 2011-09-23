var S	= {
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
		
		S.hideLoader();
	},
	
	checkEventSource											: function()
	{
		return ( 'EventSource' in window );
	},
	
	
};

$( document ).ready( S.ready );