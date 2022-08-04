import datetime

def ticks_to_datetime(ticks:int) -> datetime.datetime:
	'''
	Converts a C# System DateTime Tick into a Python DateTime
	https://gist.github.com/gamesbook/03d030b7b79370fb6b2a67163a8ac3b5
	https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=net-6.0
	Example: 637922723630700000 -> datetime.datetime(2022, 7, 1, 11, 39, 23, 70000)
	'''
	return datetime.datetime(1,1,1) + datetime.timedelta(microseconds=ticks//10)