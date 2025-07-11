PGDMP     ;                    y           vj017877_vba    13.1    13.1 "    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16451    vj017877_vba    DATABASE     q   CREATE DATABASE vj017877_vba WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United Kingdom.1252';
    DROP DATABASE vj017877_vba;
                postgres    false            �            1259    16477    admin    TABLE     p   CREATE TABLE public.admin (
    module_id character varying NOT NULL,
    user_id character varying NOT NULL
);
    DROP TABLE public.admin;
       public         heap    postgres    false            �            1259    16766 
   attendance    TABLE     �   CREATE TABLE public.attendance (
    module_id text NOT NULL,
    session_id integer NOT NULL,
    user_id character varying(8) NOT NULL,
    attendance_time timestamp without time zone,
    attendance_capture character varying
);
    DROP TABLE public.attendance;
       public         heap    postgres    false            �            1259    16517    module_sessions    TABLE     �   CREATE TABLE public.module_sessions (
    session_id bigint NOT NULL,
    module_id text NOT NULL,
    session_date timestamp without time zone NOT NULL,
    session_name character varying NOT NULL
);
 #   DROP TABLE public.module_sessions;
       public         heap    postgres    false            �            1259    16758    module_sessions_session_id_seq    SEQUENCE     �   ALTER TABLE public.module_sessions ALTER COLUMN session_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.module_sessions_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    205            �            1259    16471    modules    TABLE     �   CREATE TABLE public.modules (
    module_id character varying(8) NOT NULL,
    module_name character varying(250) NOT NULL,
    module_threshhold integer DEFAULT 0 NOT NULL,
    module_timestamp_registered timestamp without time zone
);
    DROP TABLE public.modules;
       public         heap    postgres    false            �            1259    16457    permissions    TABLE     r   CREATE TABLE public.permissions (
    permission_id bigint NOT NULL,
    permission_name character varying(25)
);
    DROP TABLE public.permissions;
       public         heap    postgres    false            �            1259    16555    permissions_permission_id_seq    SEQUENCE     �   ALTER TABLE public.permissions ALTER COLUMN permission_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.permissions_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    201            �            1259    16452    users    TABLE     w  CREATE TABLE public.users (
    user_id character varying NOT NULL,
    permissions_id integer NOT NULL,
    user_name character varying(250) NOT NULL,
    user_password character varying(250) NOT NULL,
    user_video_location character varying(250) NOT NULL,
    user_timestamp_registered timestamp without time zone NOT NULL,
    user_biometric_consent boolean NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16492    users_modules    TABLE     �   CREATE TABLE public.users_modules (
    module_id character varying(8) NOT NULL,
    user_id character varying(8) NOT NULL,
    attendance_flag boolean NOT NULL
);
 !   DROP TABLE public.users_modules;
       public         heap    postgres    false            R           2606    16791    attendance attendance_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_pkey PRIMARY KEY (session_id, user_id);
 D   ALTER TABLE ONLY public.attendance DROP CONSTRAINT attendance_pkey;
       public            postgres    false    208    208            P           2606    16524 $   module_sessions module_sessions_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.module_sessions
    ADD CONSTRAINT module_sessions_pkey PRIMARY KEY (session_id);
 N   ALTER TABLE ONLY public.module_sessions DROP CONSTRAINT module_sessions_pkey;
       public            postgres    false    205            G           2606    16476    modules modules_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (module_id);
 >   ALTER TABLE ONLY public.modules DROP CONSTRAINT modules_pkey;
       public            postgres    false    202            E           2606    16461    permissions permissions_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (permission_id);
 F   ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_pkey;
       public            postgres    false    201            M           2606    16765     users_modules users_modules_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.users_modules
    ADD CONSTRAINT users_modules_pkey PRIMARY KEY (module_id, user_id);
 J   ALTER TABLE ONLY public.users_modules DROP CONSTRAINT users_modules_pkey;
       public            postgres    false    204    204            C           2606    16711    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    200            H           1259    16743    fki_module_id    INDEX     D   CREATE INDEX fki_module_id ON public.admin USING btree (module_id);
 !   DROP INDEX public.fki_module_id;
       public            postgres    false    203            J           1259    16516    fki_module_id_modules    INDEX     T   CREATE INDEX fki_module_id_modules ON public.users_modules USING btree (module_id);
 )   DROP INDEX public.fki_module_id_modules;
       public            postgres    false    204            N           1259    16530    fki_module_id_session    INDEX     V   CREATE INDEX fki_module_id_session ON public.module_sessions USING btree (module_id);
 )   DROP INDEX public.fki_module_id_session;
       public            postgres    false    205            A           1259    16467    fki_permission_id    INDEX     M   CREATE INDEX fki_permission_id ON public.users USING btree (permissions_id);
 %   DROP INDEX public.fki_permission_id;
       public            postgres    false    200            I           1259    16752    fki_user_id    INDEX     @   CREATE INDEX fki_user_id ON public.admin USING btree (user_id);
    DROP INDEX public.fki_user_id;
       public            postgres    false    203            K           1259    16510    fki_user_id_modules    INDEX     P   CREATE INDEX fki_user_id_modules ON public.users_modules USING btree (user_id);
 '   DROP INDEX public.fki_user_id_modules;
       public            postgres    false    204            T           2606    16744    admin module_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT module_id FOREIGN KEY (module_id) REFERENCES public.modules(module_id) NOT VALID;
 9   ALTER TABLE ONLY public.admin DROP CONSTRAINT module_id;
       public          postgres    false    202    203    2887            Y           2606    16774    attendance module_id_attendance    FK CONSTRAINT     �   ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT module_id_attendance FOREIGN KEY (module_id) REFERENCES public.modules(module_id) NOT VALID;
 I   ALTER TABLE ONLY public.attendance DROP CONSTRAINT module_id_attendance;
       public          postgres    false    208    2887    202            V           2606    16511    users_modules module_id_modules    FK CONSTRAINT     �   ALTER TABLE ONLY public.users_modules
    ADD CONSTRAINT module_id_modules FOREIGN KEY (module_id) REFERENCES public.modules(module_id) NOT VALID;
 I   ALTER TABLE ONLY public.users_modules DROP CONSTRAINT module_id_modules;
       public          postgres    false    202    204    2887            X           2606    16525 !   module_sessions module_id_session    FK CONSTRAINT     �   ALTER TABLE ONLY public.module_sessions
    ADD CONSTRAINT module_id_session FOREIGN KEY (module_id) REFERENCES public.modules(module_id) NOT VALID;
 K   ALTER TABLE ONLY public.module_sessions DROP CONSTRAINT module_id_session;
       public          postgres    false    205    2887    202            S           2606    16462    users permission_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT permission_id FOREIGN KEY (permissions_id) REFERENCES public.permissions(permission_id) NOT VALID;
 =   ALTER TABLE ONLY public.users DROP CONSTRAINT permission_id;
       public          postgres    false    2885    200    201            [           2606    16784     attendance session_id_attendance    FK CONSTRAINT     �   ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT session_id_attendance FOREIGN KEY (session_id) REFERENCES public.module_sessions(session_id);
 J   ALTER TABLE ONLY public.attendance DROP CONSTRAINT session_id_attendance;
       public          postgres    false    208    2896    205            U           2606    16753    admin user_id    FK CONSTRAINT     {   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;
 7   ALTER TABLE ONLY public.admin DROP CONSTRAINT user_id;
       public          postgres    false    200    203    2883            Z           2606    16779    attendance user_id_attendance    FK CONSTRAINT     �   ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT user_id_attendance FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 G   ALTER TABLE ONLY public.attendance DROP CONSTRAINT user_id_attendance;
       public          postgres    false    200    208    2883            W           2606    16717    users_modules user_id_modules    FK CONSTRAINT     �   ALTER TABLE ONLY public.users_modules
    ADD CONSTRAINT user_id_modules FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;
 G   ALTER TABLE ONLY public.users_modules DROP CONSTRAINT user_id_modules;
       public          postgres    false    204    2883    200           