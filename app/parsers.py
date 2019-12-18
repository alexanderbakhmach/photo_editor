from . import reqparse

sign_up_parser = reqparse.RequestParser()
sign_up_parser.add_argument('email',
                            help='This field cannot be blank',
                            required=True)
sign_up_parser.add_argument('password',
                            help='This field cannot be blank',
                            required=True)

verify_parser = reqparse.RequestParser()
verify_parser.add_argument('email_token',
                           help='This field cannot be blank',
                           required=True)

sign_up_parser.add_argument('password',
                            help='This field cannot be blank',
                            required=True)

sign_in_parser = reqparse.RequestParser()
sign_in_parser.add_argument('email',
                            help='This field cannot be blank',
                            required=True)
sign_in_parser.add_argument('password',
                            help='This field cannot be blank',
                            required=True)

sign_in_social_parser = reqparse.RequestParser()
sign_in_social_parser.add_argument('social_provider',
                                   help='This field cannot be blank',
                                   required=True)
sign_in_social_parser.add_argument('social_data',
                                   help='This field cannot be blank',
                                   required=True,
                                   type=dict)
