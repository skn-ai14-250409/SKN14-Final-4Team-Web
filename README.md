# SKN14-Final-4Team-Web
## 미니콘다 환경 세팅 방법

1. 원하는 이름으로 콘다 환경 생성
    ```commandline
    conda create -n vogue_me_env python=3.12 -y
    conda activate vogue_me_env
    ```
2. requirements.txt 가 있는 경로로 이동.
   ```commandline
   cd requirements.txt가_있는_폴더_경로
   ```
3. 패키지 설치
```commandline
pip install -r requirements.txt
```

## DB migration 주의사항
1. python manage.py makemigrations && python manage.py migrate 실행 후  
   반드시 **`default_record.sql`** 파일의 쿼리를 실행해서 mainapp_influencer 테이블에 기본 레코드가 들어가있도록 해야 한다.  
   mainapp_influencer 에 id=1 인 기본 레코드가 이미 있다면 수행하지 않아도 됨.


## 개인적으로 느낀점 정리
### 1. github action 과 docker build, Elastic beanstalk 로 CI/CD 를 구성할 때는,  
   1. 운영환경에서 docker build 를 우선 해보고, 
   2.운영환경에서 docker image 를 받아서 container 로 수행해보고,
   3. 그게 잘 되면 그 때 github action 으로 넘어가서 yml 을 만드는게 좋겠다.  
      => 왜냐,  
      github action runner 에서 docker build 를 하게 되면, requirements.txt 를 설치해야 하는데,  
      docker build 를 실패할 때마다 requirements.txt install 이라는 불필요한 과정이 소요되게 된다.  
      10초면 끝날 확인이 40초씩 걸리는 마법에 걸린다.
   
### 2. 만약 github action runner 로 django makemigrations 와 migrate 를 하려고 migrate 계정을 분리관리한다면,  
   계정의 권한은 이렇게 하는게 좋을거다.   
   ```sql
   create schema `20250901_looplabel` collate utf8mb4_general_ci;
   
   create user csr identified by '비밀번호';
   grant alter, create, delete, drop, insert, select, update on `20250901_looplabel`.* to 'csr'@'%';
   
   create user website identified by '비밀번호';
   grant delete, insert, select, update on `20250901_looplabel`.* to 'website'@'%';
   
   create user migrater identified by '비밀번호';
   grant all privileges on `20250901_looplabel`.* to 'migrater'@'%';
   
   FLUSH PRIVILEGES;
   ```  
   => 왜냐,  
   migrater 계정에 처음에는 create, alter, drop 만 줬는데, github action을 재실행할 때마다 오류가 계속 추가된다....
   1. 처음엔 insert 가 필요하단다.   그래서 create, alter, drop, insert 를 주고 다시 재실행을 했다...
   2. 그랬더니 select 도 달란다.     그래서 create, alter, drop, insert, select 를 주고 다시 재실행을 했다...
   3. 그랬더니 references 도 달란다. 그래서 create, alter, drop, insert, select, references 를 주고 다시 재실행을 했다...
   4. 그랬더니 뭘 또 달래. 안되겠다 싶기도 했고, github action 에서만 사용할 계정이라서 all privileges 로 줘버렸다. 
### 3. 새로운 beanstalk 환경에 소스를 배포할 때마다 로그인/회원가입을 하려고 하면 500 에러가 났다.  
   => 알고보니 DB 접속이나 이메일 발송시스템 등 환경변수를 필요로 하는 녀석들이 있는데,  beanstalk 에 환경변수가 등록이 안되어있는 거였다.
4. 
