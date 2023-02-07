from database.engine import engine
from database.models import Request
from sqlalchemy.orm import Session

with Session(engine) as session:
    for i in range(10):
        request_one = Request(
            from_title="test" + str(i),
            from_namespace=0,
            to_title="to page" + str(i),
            to_namespace=0,
            request_type=1,
        )
        session.add(request_one)
        session.commit()
