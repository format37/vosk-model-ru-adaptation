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
	words['model'] = 1
	words['corpus'] = 0
	response  = words.to_csv(header = True, index = False, sep=";")
	return web.Response(text=response,content_type="text/html")


async def call_download_merged(request):
	words = pd.read_csv('model_files/corpus.txt', header=None)
	words.columns = ['word']
	response  = words.to_csv(header = True, index = False, sep=";")
	return web.Response(text=response,content_type="text/html")


async def call_upload_corpus(request):
	csv_text = str(await request.text()).replace('\ufeff', '')
	with open('model_files/corpus_batch_'+str(uuid.uuid4())+'.csv', 'w') as f:
		f.write(csv_text)
	return web.Response(text='Upload successfull',content_type="text/html")


async def call_merge_corpus(request):
	# read corpus
	path = 'model_files/'
	files = [f for f in os.listdir(path) if f.startswith('corpus_batch_')]
	corpus = pd.DataFrame()
	for f in files:
		corpus = corpus.append(pd.read_csv(path+f))
	# drop duplicates
	corpus = corpus.drop_duplicates()
	# read words
	words = pd.read_csv(path+'words.txt', sep=" ")
	words.columns = ['word', 'id']
	words.drop(['id'], axis=1, inplace=True)
	# drop contained in dictionary words
	corpus = corpus[~corpus.word.isin(words.word)]
	corpus.word = corpus.word.str.lower()
	if len(corpus):
		# save merged corpus for download to user databases
		corpus.to_csv(path+'corpus.txt', header=None, index = False)
		# unlink temporary dictionary files
		for dict_file in os.listdir(path+'corpus/'):			
			os.unlink(path+'corpus/'+dict_file)
		# save merged corpus for model dictionary update
		corpus.to_csv(path+'corpus/corpus.txt', header=None, index = False)
	# unlink temporary source corpus files
	for f in files:
		os.unlink(path+f)
	return web.Response(text='Merge successfull',content_type="text/html")


def main():
	app = web.Application(client_max_size=1024**3)
	app.router.add_route('GET', '/test', call_test)
	app.router.add_route('GET', '/download_dictionary', call_download_dictionary)
	app.router.add_post('/upload_corpus', call_upload_corpus)
	app.router.add_route('GET', '/merge_corpus', call_merge_corpus)
	app.router.add_route('GET', '/download_merged', call_download_merged)

	web.run_app(
		app,
		port=os.environ.get('PORT', ''),
	)


if __name__ == "__main__":
    main()
