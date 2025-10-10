# Instructions to fix the permissions issue

The service principal does not have the required permissions to create role assignments. To fix this, you need to assign the `User Access Administrator` role to the service principal at the subscription level.

Here is the command to do that:

```bash
az role assignment create --assignee "d8b0b1e1-e87e-49fd-ae3b-b0ef21376c8e" --role "User Access Administrator" --scope "/subscriptions/fc8ae4ba-e0af-47b8-971a-4792f7399cf3"
```

After you run this command, the service principal will have the necessary permissions to create role assignments, and the Terraform commands should run successfully.