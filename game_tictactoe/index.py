import pusher

pusher_client = pusher.Pusher(
  app_id='1193552',
  key='797cf18b328b54dede0e',
  secret='eb6dcea8fba67a8e13d9',
  cluster='ap1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})