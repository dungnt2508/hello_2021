#hello_2021 : app quan ly
  + app_demo
    + api
      - __init__.py
      - models.py
      - routes.py
    + build
      + static
        + config
        + dist
        + js
        + npm
        + plugins
        + scss
      + templates
        + auth
          - login.html
          - register.html
        + page
          - dashboard.html
    - __init__.py
    - db.py
  + instance
    - .ini
    - config.py
  - main.py
  - README.md


--------------------------------------------------------------------------------------------------
part 1 : 
    - build skeleton for app 
    - config app
    - connect db
    - build auth system :
            register
            login
            logout
            load_logged_in_user
    - build auth view :
            register
            login
            
            
--------------------------------------------------------------------------------------------------
part qlcamdo : 
    - build skeleton for app quan ly : done
    - config app : done
    - connect db : done
    - build auth system :
            register : done
            login : done
            
    - build auth view :
            register : done
            login : done
     - build page view : 
            dashboard : doing


----------------------------------------------------------
- tên app : vietgold


+ module user :	/user
		- đăng ký:	/register  --80%
		- đăng nhập	/login  --80%
		- thông tin giao dịch : theo ngày , tuần, năm	/user_id
		
+ module khách hàng : /customer
		- thông tin khách hàng : tên, giấy tờ, tài sản, sdt, ghi chú	/customer_id
		- tạo 	/create
		- sửa : thêm giấy tờ	/update/customer_id
		- xóa	/delete/customer_id


+ module hóa đơn : /invoice
		- danh sách hợp đồng : người soạn hợp đồng, ngày tạo, thông tin khách hàng, tài sản, lãi suất, tiền thu, tiền chi, ghi chú 
		- chi tiết hợp đồng	/invoice_id
		- tạo /create
		- sửa /update
		- xóa /delete

+ module cấu hình :	/setting
		- chi tiết phí	/rates	-- Nghiệp vụ  
		- phân quyền 	/rules	


+ module báo cáo : /dashboard
		- báo cáo thông tin tài sản cần tất toán , thu chi
  
- hóa đơn cầm đồ -> thanh toán lãi , tất toán , thanh lý, bán
