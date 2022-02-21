from setup.properties import *

def is_authorised(ctx, authorizedRolesIds):
	roleIds = [role.id for role in ctx.author.roles]
	authorizedRoles = list({key: roles[key] for key in authorizedRolesIds}.values())
	roleExists = [value for value in authorizedRoles if value in roleIds]
	return len(roleExists) > 0

def is_founders(ctx):
	return is_authorised(ctx, {'founders'})
