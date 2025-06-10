-- Banks Table
create table banks (
   bank_id      number primary key,
   bank_name    varchar2(100) not null unique,
   created_date date default sysdate
);

-- Reviews Table (only columns from processed_reviews.csv)
create table reviews (
   review_id      number primary key,
   bank_id        number
      references banks ( bank_id ),
   review_text    clob,
   rating         number(3,1),
   review_date    date,
   source         varchar2(50),
   processed_date date default sysdate,
   constraint fk_bank foreign key ( bank_id )
      references banks ( bank_id )
);

-- Create sequence for IDs
create sequence bank_seq start with 1 increment by 1;
create sequence review_seq start with 1 increment by 1;