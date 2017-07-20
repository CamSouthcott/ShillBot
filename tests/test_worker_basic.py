
import unittest
import codecs
import os

from workers.basic_worker import BasicUserParseWorker, WorkerException


class TestWorkerBasic(unittest.TestCase):

    def test_basic_worker_connection(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(ConnectionRefusedError, worker.run)

    def test_worker_parsing(self):
        """
        Purpose: Test regular parsing mechanisms of worker
        Expectation: Load html file, send it to worker to parse, should return list of results

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        file_path = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'test_resources/sample_GET_response.html')

        with codecs.open(file_path, encoding='utf-8') as f:
            text = f.read()

        results, next_page = worker.parse_text(str(text).strip().replace('\r\n', ''))

        self.assertGreater(len(results), 0)     # Check that results are returned
        self.assertEqual(len(results[0]), 3)    # Check that results are in triplets (check formatting)

    def test_worker_add_links_max_limit(self):
        worker = None
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 0
        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links("test.com")
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before)
        
    #adds an empty list to the to_crawl list, should do nothing
    def test_worker_add_links_empty_list(self):
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        
        before_links = len(worker.to_crawl)
        worker.add_links([])
        after_links = len(worker.to_crawl)
        
        self.assertEqual(before_links, after_links)
        
    #general add_links test, puts 5 links in the list and then adds a list of 5 other links to it
    def test_worker_add_links(self):
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 10
        
        for i in range(5):
            worker.add_links(['link' + str(i)])
            
        self.assertEqual(len(worker.to_crawl), 5)
        
        links_list = []
        for i in range(5,10):
            links_list.append('link' + str(i))
            
        worker.add_links(links_list)
        
        self.assertEqual(len(worker.to_crawl), 10)
        
    #send worker to nonexistant url
    def test_worker_bad_url(self):
        worker = BasicUserParseWorker('https://www.slkdfjasdlwrwqerwerwerwer.com')
        
        #worker should raise a WorkerException trying to get data from a nonexistant url
        self.assertRaises(WorkerException, worker.run)







