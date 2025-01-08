# # import session
# from database.databaseConfig.databaseConfig import SessionLocal

# # Import Entities
# from database.entity.Plan import Plan
# from database.entity.Occupation import Occupation
# from database.entity.Coupon import Coupon

# def seed_coupon():
#     session = SessionLocal()
#     coupon = Coupon('GWBFC0011', 10, 10)
#     dbcoupon = session.query(Coupon).filter_by(code=coupon.code).first()
#     if dbcoupon == None:
#         session.add(coupon)
#         session.commit()
#         session.flush()
#     session.close()

# session = SessionLocal()
# coupon = Coupon('GBF099', 99.90, 90)
# dbcoupon = session.query(Coupon).filter_by(code=coupon.code).first()
# if dbcoupon == None:
#     session.add(coupon)
#     session.commit()
#     session.flush()
# session.close()

# def seed_prefession():
#     session = SessionLocal()
#     ocu = Occupation(1, 'Engineer')
#     ocuserv = session.query(Occupation).filter_by(id=1).first()
#     if ocuserv == None:
#         session.add(ocu)
#         session.commit()
#         session.flush()
#     session.close()

# def seed_plans():
#     session = SessionLocal()
#     plans = session.query(Plan).all()
#     if len(plans) == 0:
#         plan = Plan('Basic', 14.99, 170, 90, 3, '1 License$50 web pages design$Last 5 days History$Chat Support$5 Web-Framework support$AI Chat Support$Discord Support')
#         plan1 = Plan('Pro', 29.99, 330, 180, 6, '1 License$120 web pages design$Last 15 days History$Early Access to new Features$Priority Feature Requests$Chat Support$5+ Web-Framework support$AI Chat Support$Discord Support')
#         plan2 = Plan('GOLD', 51.99, 550, 365, 12, '1 License$250 web pages design$Last 1 Month History$Early Access to new Features$Priority Feature Requests$Chat Support$5+ Web-Framework support$AI Chat Support$Discord Support')
#         session.add(plan)
#         session.add(plan1)
#         session.add(plan2)
#     else:
#         for pl in plans:
#             if pl.numoftokens == 50:
#                 pl.numoftokens = 170
#             elif pl.numoftokens == 120:
#                 pl.numoftokens = 330
#             elif pl.numoftokens == 250:
#                 pl.numoftokens = 550

#     session.commit()
#     session.flush()
#     session.close()
    
# def seed_all():
#     seed_prefession()
#     seed_plans()
#     seed_coupon()