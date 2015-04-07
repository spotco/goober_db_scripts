package 
{
	import flash.display.Sprite;
	import flash.events.Event;
	
	/**
	 * ...
	 * @author spotco
	 */
	[SWF(width = "500", height = "520", frameRate = "60", backgroundColor = "#FFFFFF")]
	[Frame(factoryClass="Preloader")]
	public class Main extends Sprite 
	{
		[Embed( source = "../resc/jumpdiecreate.swf" )]
		private static var JumpDieCreateGame:Class;
		public function Main():void 
		{
			trace("fuck");
			if (stage) init();
			else addEventListener(Event.ADDED_TO_STAGE, init);
		}
		
		private function init(e:Event = null):void 
		{
			removeEventListener(Event.ADDED_TO_STAGE, init);
			// entry point
			this.addChild(new JumpDieCreateGame);
		}
		
	}
	
}