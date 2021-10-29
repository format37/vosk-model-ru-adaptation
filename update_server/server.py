from aiohttp import web
import os
import pandas as pd
from io import StringIO
import uuid

async def call_test(request):
	content = "ok"
	return web.Response(text=content,content_type="text/html")


async def call_download_dictionary(request):
	words = pd.read_csv('model_files/words.txt', sep=" ")
	words.columns = ['word', 'id']
	words.drop(['id'], axis=1, inplace=True)

	#corpus = pd.read_csv('model_files/corpus.txt', header = None)
	#corpus.columns = ['word']

	words['model'] = 1
	words['corpus'] = 0
	#corpus['model'] = 0
	#corpus['corpus'] = 1

	#df = pd.concat([words, corpus], ignore_index=True)
	#df = df.groupby('word').max()

	#df.reset_index(inplace = True)
	
	#response  = df.to_csv(header = True, index = False, sep=";")
	response  = words.to_csv(header = True, index = False, sep=";")
	return web.Response(text=response,content_type="text/html")


async def call_upload_corpus(request):
	csv_text = str(await request.text()).replace('\ufeff', '')
	with open('model_files/corpus_batch_'+str(uuid.uuid4())+'.csv', 'w') as f:
		f.write(csv_text)

	return web.Response(text='Upload successfull',content_type="text/html")


async def call_merge_corpus(request):
	path = 'model_files/'
	files = [f for f in os.listdir(path) if f.startswith('corpus_batch_')]
	df = pd.DataFrame()
	for f in files:
		df = df.append(pd.read_csv(path+f, index_col=0))
	df = df.drop_duplicates()	
	
	return web.Response(text='Merge successfull',content_type="text/html")


def main():
	app = web.Application(client_max_size=1024**3)
	app.router.add_route('GET', '/test', call_test)
	app.router.add_route('GET', '/download_dictionary', call_download_dictionary)
	app.router.add_post('/upload_corpus', call_upload_corpus)
	app.router.add_route('GET', '/merge_corpus', call_merge_corpus)

	web.run_app(
		app,
		port=os.environ.get('PORT', ''),
	)


if __name__ == "__main__":
    main()
