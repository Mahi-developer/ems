-- create required user and new database for ems
CREATE USER ems_user WITH PASSWORD 'emsPass123';
CREATE DATABASE ems OWNER ems_user;