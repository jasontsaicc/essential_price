from elasticsearch import Elasticsearch


class elasticsearch():
    def __init__(self, index_name, index_type):
        self.es = Elasticsearch(hosts='elasticsearch', port=9200)
        self.index_name = index_name
        self.index_type = index_type

    def search(self, query, count: int = 30, page: int = 0):
        body = {
            "from": page,
            "size": 12,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["product_name"]
                }
            },
            "collapse": {
                "field": "product_name.keyword"
            }
        }
        print("body", body)
        match_data = self.es.search(index=self.index_name, doc_type=self.index_type, body=body, size=count)
        return match_data

    def shop_details_search(self, query, count: int = 30):
        body = {
            "from": 0,
            "size": 5,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["product_name"]
                }
            },
            "collapse": {
                "field": "product_name.keyword"
            }
        }
        print("body", body)
        match_data = self.es.search(index=self.index_name, doc_type=self.index_type, body=body, size=count)
        return match_data
