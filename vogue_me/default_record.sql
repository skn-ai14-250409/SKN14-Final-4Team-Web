/* DB 에 무조건 하나는 있어야 하는 데이터. */
insert into mainapp_influencer(name, profile_img_url) values('진경', 'https://elasticbeanstalk-ap-northeast-2-967883357924.s3.ap-northeast-2.amazonaws.com/influencer/hjk.jpeg');
update mainapp_influencer set id=1 where name='진경' and id != 1;


insert into mainapp_influencer(name, profile_img_url) values('우재', 'https://entertainimg.kbsmedia.co.kr/cms/uploads/PERSON_20211106192257_a217bf5cd095fa333c151af28235bbd7.jpg');
insert into mainapp_influencer(name, profile_img_url) values('혜진', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQa7D2z6saPFqTgN-XqFiYc_gZ9eTJ_yq3d0w&s');
insert into mainapp_influencer(name, profile_img_url) values('호영', 'https://elasticbeanstalk-ap-northeast-2-967883357924.s3.ap-northeast-2.amazonaws.com/influencer/lhy.jpeg');

update mainapp_influencer set id=2 where name='우재' and id != 2;
update mainapp_influencer set id=3 where name='혜진' and id != 3;
update mainapp_influencer set id=4 where name='호영' and id != 4;

