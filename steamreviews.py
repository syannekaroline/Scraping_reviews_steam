# pré-requisito --> instalar pacote : pip install steam-review-scaper

import steamreviews

request_params = dict()
# Reference: https://partner.steamgames.com/doc/store/localization#supported_languages
request_params['language'] = 'english'
# Reference: https://partner.steamgames.com/doc/store/getreviews
request_params['review_type'] = 'positive'
request_params['purchase_type'] = 'steam'

app_id = 573170
review_dict, query_count = steamreviews.download_reviews_for_app_id(app_id, chosen_request_params=request_params)
