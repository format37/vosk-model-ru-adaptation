from aiohttp import web
import os
import pandas as pd

async def call_test(request):
	content = "ok"
	return web.Response(text=content,content_type="text/html")


async def call_read_words(request):
	df = pd.DataFrame()
	response  = df.to_csv(sep=';', index = False)
	return web.Response(text=response,content_type="text/html")	


def main():
	app = web.Application(client_max_size=1024**3)
	app.router.add_route('GET', '/test', call_test)
	app.router.add_route('GET', '/read_words', call_read_words)

	web.run_app(
		app,
		port=os.environ.get('PORT', ''),
	)


if __name__ == "__main__":
    main()
