
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# from firebase_admin import credentials


# def firefunc():
#     cd = credentials.Certificate(
#         {
#         "type": "service_account",
#     "project_id": "firedjang",
#     "private_key_id": "6c1d9c1a5752f1c7cb954da924519b4a8ded9824",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDEdZto8uR1o9Ir\nKTmDqiHDZAbZeoKrxEapumg9htNF4QnIer0qoWh6SZ87CSwKOJtYEvNIYOFu3mEG\nUad4MDuNruZT2avf0uzzWiPjbiPfhlVpd91hhskWkos38eM4BPIhlH1It3EXQVqL\nQxQ8NReTOMraGYjQ6/8xzIxT0pYM3p7PSRQMBjI8koa6uEnFprSx6gR07P09uS2A\nDIfdl94cNJd95WKifoGUhtwcsholm0cPnzon3y3bsS0ghi5hqC/P12Jk2pgR6SQW\n6/b/NyJlhk2pjef13bTrJeUZUj6Cze8xqMcrFxh8QeYAHZSjxXdFpg7Z0crAGDgl\nABT7Lei7AgMBAAECggEAAZz6b76A93SQXCaqIGKuDJbWAReTw+AxwLOvpstVPp2A\n8iZmsAR8hQ1AW9sB3dXa3aQDXzlWFFHVrk0LK7xGmOnqqUNtV1FBdZySFNAYr/X8\ng9r82h7lt4X/iCD72ho7Wmh40z7FMrKKa5bbZADwMQCNw/yIkqGrHP3G6J9MQ7dr\n/Kz39OViDvB3D5UM9oVhX8MD8jwIQrIe6M+lkB7mWN28bv5vTbbR8sUsgXTnKpR4\nM4bRbyx0RqXygmPmF5YPeIggD2w8XNT917x7D0bXZJ+QOL672g2E33C366/vH1UC\noey47eF9bkHy4pf1FMW6qDJB3jmHpgXnJ4SDcjAaCQKBgQDqgaY3zZSXLx/thj1r\nRBNiGw5VCVGmJPz3mNOx8dbGhUqNj+BPI4jJl+iEZC4yJbj607KcBVrhTs5Gu29X\n5nkYzxY90vFugd25vlGG5g0f/Qe90NIurDD4iZO2CfeUZ+USQsK7wnosoqHiJ7PF\npj0+JXQtS0Ljznw4Avbn5RV94wKBgQDWdz1YlGKSmjCLjg47khNr5unQxM/dvS0c\n4IkQ6D8EB2vR7MRrpAGP4vTKO+VImqJAXwiMkMs3nMzby/gtWMM3oQIBSfPJMytY\nM+6Uwla6nw2u8U8wTUo+emsS+3GPmtNVSjSQSqA+MoqjZZAseCUO1lx32L87jWge\nverxrl5hSQKBgCXoY1gt8VEnGwAobRFD5eY7/WsdoIc8/29+0um28EMTFOQhV98z\nHU+JMNsF3rnYgzh4tCyoaPJ27L1eWzdYWEb8YtoHmWOFtrPp4f/ufDypiHDUqsVE\nrH3gr3ID1nO0/8Cd7iCv5VQFzilixZqzrr63CzqvKdbtcAMV55fA3mKFAoGBAIB+\n3NCPxyeTHnbe3AQxF1XU+k5NPUXbrIXaugTZQbhGQgF63IyprQ3qq0Pn8w43J/Nt\nfQ/LSRa+6bbfVIjG3+Aapbrj9h6ce+HS66VRculJlsc0aX/FLzCT5EdxQ68I0ooN\ndcTmEXByk8ImfeVG7t0e7jQYNyuVI8cXfwbitEWRAoGARhx4kt2XXr09WbzQ/pnT\nDu80hT6eMQGMZ1HJlw3j8eBpN0vs8Hx6HsN4bqejyQ8ij9Wh4NsSQ3XqtBH+7wcS\n5TKG/m7js4+3pVLZ+PjMbefwFvx1cefy/NbcySTw+9K79BqsnPxwmxJ3lKQkWOL2\nkxMKG12sL/hchaaRUCHAMLE=\n-----END PRIVATE KEY-----\n",
#     "client_email": "firebase-adminsdk-lri3f@firedjang.iam.gserviceaccount.com",
#     "client_id": "114260328089911705184",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-lri3f%40firedjang.iam.gserviceaccount.com"
#     }
#     )

#     firebase_admin.initialize_app(cd)
#     datab = firestore.client()




#         # # firebase_admin.initialize_app()
#         # if not firebase_admin._apps: # Note the underscore
#         #     firebase_admin.initialize_app()
#         # datab = firestore.client()


#     doc_ref = datab.collection(u'usersInfo').document(u'ID5')
#     doc_ref.set({
#     u'first': u'nash',
#     u'last': u'babb',
#     })
#     print("hey")
