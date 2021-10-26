from aiohttp import web
import os
import pandas as pd

async def call_test(request):
	content = "ok"
	return web.Response(text=content,content_type="text/html")


async def call_read_words(request):
	words = pd.read_csv('model_files/words.txt', sep=" ")
	words.columns = ['word', 'id']
	words.drop(['id'], axis=1, inplace=True)

	corpus = pd.read_csv('model_files/corpus.txt', header = None)
	corpus.columns = ['word']

	words['model'] = 1
	words['corpus'] = 0
	corpus['model'] = 0
	corpus['corpus'] = 1

	df = pd.concat([words, corpus], ignore_index=True)
	
	response  = df.to_csv(header = False, index = False)
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
