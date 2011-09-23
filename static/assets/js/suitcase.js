var S	= {
	ready														: function()
	{
		if ( S.checkEventSource() )
		{
			
		}
		else
		{
			
		}
	},
	
	checkEventSource											: function()
	{
		return ( 'EventSource' in window );
	}
};

$( document ).ready( S.ready );