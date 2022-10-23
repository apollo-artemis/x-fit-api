

def custom_commit(item, session):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
    except:
        pass

