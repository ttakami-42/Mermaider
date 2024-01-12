import requests
from base64 import b64encode
from furl import furl
from .exc import ModalException

def getImageURL(mermaid: str, darkmode: int) -> str:
	colorset = "%%{init:{'theme':'dark'}}%%" if darkmode else "%%{init:{'theme':'forest'}}%%"
	before = f'{colorset}\n{mermaid}'
	try:
		base64EncodedString = b64encode(before.encode()).decode()
		imageURL = furl('https://mermaid.ink/img/')
		imageURL.path.add(base64EncodedString)
		if darkmode:
				imageURL.args['bgColor'] = '1E1F22'
		return (imageURL.url)
	except Exception as e:
		raise ModalException(e, "Image URL")

def isImageURL(url: str) -> bool:
	try:
		response = requests.head(url)
		if response.status_code == requests.codes.ok:                                        # Success
			return (True)
		elif response.status_code in [requests.codes.bad_request, requests.codes.not_found]: # ChatGPT might generate wrong Mermaid code
			return (False)
		else:                                                                                # API, Network, Server, or something else's error
			response.raise_for_status()
	except Exception as e:
		raise ModalException(e, "API [2]")
