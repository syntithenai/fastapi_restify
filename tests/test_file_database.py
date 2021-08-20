import asyncio
# list get insert update delete
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")

from file_database import FileDatabase

def test_file_database():
    filename = "/tmp/testdata.json"
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    
    async def do_test():
        db = FileDatabase(filename)
        # insert
        await db.insert({'name':'fred', 'sex':'M'})
        results = await db.list()
        assert(len(results) == 1)
        assert(results[0]['name'] == 'fred')
        assert(results[0]['sex'] == 'M')
        # get
        single = await db.get(results[0]['_id'])
        assert(single['name'] == 'fred')
        # find
        findresults = await db.find({'name':'fred'})
        assert(findresults[0]['name'] == 'fred')
        assert(findresults[0]['sex'] == 'M')
        assert(len(findresults) == 1)
        # replace
        await db.replace(results[0]['_id'], {'name':'bill', 'age':33})
        checkresults = await db.list()
        assert(len(checkresults) == 1)
        assert(checkresults[0]['name'] == 'bill')
        assert(checkresults[0]['age'] == 33)
        assert(checkresults[0].get('sex', None) == None)  # sex was cleared by replacement
        # update
        await db.update(results[0]['_id'], {'name':'joe'})
        checkresults = await db.list()
        assert(len(checkresults) == 1)
        assert(checkresults[0]['age'] == 33) # age unchanged
        assert(checkresults[0]['name'] == 'joe')
        # delete        
        results = await db.delete(results[0]['_id'])
        assert(results == True)
        results = await db.list()
        assert(len(results) == 0)

    asyncio.run(do_test())

if __name__ == "__main__":
    test_file_database()
