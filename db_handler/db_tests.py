from db_handler import DatabaseHandler
import pandas as pd
from sqlalchemy import exc

if __name__ == '__main__':
    # unittest.main()
    try:
        db = DatabaseHandler('test')
    except exc.OperationalError:
        db = DatabaseHandler()

#    db.create_db('test')
    test_df = pd.DataFrame(data=['foo', 'bar', 'foofoo', 'barbar'])
    test_df.to_sql('test',db.connection,if_exists='replace')
    results = db.query('SELECT * FROM test')
    for result in results:
        print(result)
