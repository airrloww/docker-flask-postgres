test connection:
```bash
curl http://localhost:5000/test
```
create users:
```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"email\":\"email1@example.com\"}"
```
```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d "{\"username\":\"user2\",\"email\":\"email2@example.com\"}"
```
get all users:
```bash
curl -X GET http://localhost:5000/users
```
update user:
```bash
curl -X PUT http://localhost:5000/users/2 -H "Content-Type: application/json" -d "{\"username\":\"user3\",\"email\":\"email3@example.com\"}"
```
delete user:
```bash
curl -X DELETE http://localhost:5000/users/1
```
aloooooooooooo