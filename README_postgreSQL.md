 



## Sign-in
Sign in with the current signed in user (default) 
    
    >> ssh artinmajdi@data7-db1.cyverse.org -p 1657
    >> ssh artinmajdi@128.196.65.115 -p 1657
    
    >> psql -U postgres
    >> password: 1234

Go into a specific database & a specific user:     
    
    psql -d mlflow_db -U mlflow_user
    psql postgres -h 128.196.65.115 -p 1657 -U artinmajdi

## List users/databases/info
Show Users:                           
    
    \du
   
list all databases                    
    
    \l


## Creating new user (a.k.a. role)
Create a new role with a username and password: 
                              
    CREATE USER <username> WITH ENCRYPTED PASSWORD <password> LOGIN SUPERUSER;
   
Delete a user 

    DROP USER <username>

### Grant Access to a table/database
Grant access to a database                      
   
    GRANT <privilege_list or ALL>  ON  DATABASE <database_name> TO  <username>;

Grant access to a table                      
    
    GRANT <privilege_list or ALL>  ON  <table_name> TO  <username>;
   
Revoke all privileges

    REVOKE ALL PRIVILEGES on DATABASE <database_name> FROM <user>;

## Creating/removing new database
Create a new database:                          
    
    CREATE DATABASE [IF NOT EXISTS] <database_name>;

Delete a database permanently:                  
    
    DROP DATABASE [IF EXISTS] <database_name>;

vim databse
    
    ALTER DATABASE name RENAME TO new_name

Change ownership
    
    ALTER DATABASE name OWNER TO new_owner

## Viewing tables
Connect to a specific database:       
   
    \c database_name;
   
Showing information on database name, username, port, socket path    
    
    \conninfo

list all tables in current database   
    
    \dt   or \dt+ (for more information)

   
Get detailed information on a table:  
    
    \d+ table_name
   
View all data inside a table:                    
    
    SELECT * FROM table_name;



## How to get TLS version
openssl ciphers -v | awk '{print $2}' | sort | uniq

## to see the ports used in ubuntu
netstat -tuanlp


## sftp
sftp -oPort=1657 bartinmajdi@data7-db1.cyverse.org/home/artinmajdi/mlflow_data/artifact_store