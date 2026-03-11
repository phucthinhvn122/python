import requests
import os
import time
from flask import Flask, render_template_string, request, jsonify

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevThinh | Công Cụ Nâng Cao</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap"
        rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome Elements -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <style>
        :root {
            /* Brand Colors (Discord/Cyber hue) */
            --primary: #5865F2;
            --primary-hover: #4752C4;
            --secondary: #EB459E;
            --accent: #00FFC2;

            /* Backgrounds (Dark Glassmorphism) */
            --bg-darker: #0b0c10;
            --bg-glass: rgba(23, 25, 30, 0.7);
            --bg-glass-light: rgba(255, 255, 255, 0.05);
            --bg-glass-input: rgba(0, 0, 0, 0.25);

            /* Text & Borders */
            --text-main: #f2f3f5;
            --text-muted: #a3a6aa;
            --border-glass: rgba(255, 255, 255, 0.08);

            /* Glow Effects */
            --glow-primary: 0 0 25px rgba(88, 101, 242, 0.4);
            --glow-accent: 0 0 25px rgba(0, 255, 194, 0.15);
        }

        body {
            background-color: var(--bg-darker);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 30px 15px;
            overflow-x: hidden;
            position: relative;
        }

        /* Abstract Dynamic Background Elements */
        .bg-orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(100px);
            z-index: -1;
            animation: float 20s infinite ease-in-out alternate;
        }

        .orb-1 {
            width: 400px;
            height: 400px;
            background: rgba(88, 101, 242, 0.3);
            top: -100px;
            left: -100px;
        }

        .orb-2 {
            width: 500px;
            height: 500px;
            background: rgba(235, 69, 158, 0.2);
            bottom: -150px;
            right: -100px;
            animation-delay: -5s;
        }

        .orb-3 {
            width: 300px;
            height: 300px;
            background: rgba(0, 255, 194, 0.15);
            top: 30%;
            left: 40%;
            animation-delay: -10s;
        }

        @keyframes float {
            0% {
                transform: translateY(0) scale(1);
            }

            50% {
                transform: translateY(-30px) scale(1.1);
            }

            100% {
                transform: translateY(20px) scale(0.9);
            }
        }

        /* Container & Grid Layout */
        .main-container {
            width: 100%;
            max-width: 900px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            z-index: 10;
        }

        @media (min-width: 992px) {
            .main-container {
                grid-template-columns: 350px 1fr;
                /* Max width expanded for dual pane */
                max-width: 1000px;
            }
        }

        /* Global Glassmorphic Card */
        .glass-panel {
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
            padding: 25px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        /* Nav Sidebar Area */
        .nav-wrapper {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .brand {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), #a6b2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            letter-spacing: -1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-subtitle {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* Custom Modern Tabs as Sidebar Nav */
        .nav-pills-custom {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        @media (max-width: 991px) {
            .nav-pills-custom {
                flex-direction: row;
                overflow-x: auto;
                padding-bottom: 10px;
            }

            .nav-pills-custom .nav-link {
                white-space: nowrap;
                flex: 1;
                text-align: center;
            }
        }

        .nav-pills-custom .nav-link {
            border-radius: 12px;
            color: var(--text-muted);
            font-weight: 600;
            padding: 14px 20px;
            text-align: left;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            background: transparent;
            border: 1px solid transparent;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .nav-pills-custom .nav-link i {
            font-size: 1.1rem;
        }

        .nav-pills-custom .nav-link:hover {
            color: var(--text-main);
            background: var(--bg-glass-light);
            transform: translateX(5px);
        }

        .nav-pills-custom .nav-link.active {
            color: white;
            background: linear-gradient(90deg, rgba(88, 101, 242, 0.1), transparent);
            border: 1px solid var(--primary);
            box-shadow: inset 3px 0 0 var(--primary), var(--glow-primary);
        }

        /* Inputs & forms */
        .form-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .form-control {
            background-color: var(--bg-glass-input);
            border: 1px solid var(--border-glass);
            color: white;
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        .form-control::placeholder {
            color: rgba(255, 255, 255, 0.3);
        }

        .form-control:focus {
            background-color: rgba(0, 0, 0, 0.4);
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(88, 101, 242, 0.15);
            color: white;
        }

        /* Sub-pills (Login Type Toggle) */
        .sub-nav {
            background: var(--bg-glass-input);
            border-radius: 12px;
            padding: 5px;
            display: flex;
            margin-bottom: 25px;
        }

        .sub-nav .nav-link {
            flex: 1;
            text-align: center;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            transition: all 0.2s;
            cursor: pointer;
            border: none;
        }

        .sub-nav .nav-link.active {
            background: var(--bg-glass-light);
            color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Buttons */
        .btn-modern {
            padding: 14px 20px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.5px;
            width: 100%;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            border: none;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
            box-shadow: 0 5px 15px rgba(88, 101, 242, 0.3);
        }

        .btn-primary:hover,
        .btn-primary:active {
            background: var(--primary-hover) !important;
            transform: translateY(-2px);
            box-shadow: var(--glow-primary);
        }

        .btn-accent {
            background: rgba(0, 255, 194, 0.1);
            color: var(--accent);
            border: 1px solid rgba(0, 255, 194, 0.3);
        }

        .btn-accent:hover {
            background: rgba(0, 255, 194, 0.2);
            box-shadow: var(--glow-accent);
        }

        /* Special groups */
        .capsolver-group {
            background: linear-gradient(135deg, rgba(88, 101, 242, 0.05), rgba(235, 69, 158, 0.05));
            border: 1px solid rgba(88, 101, 242, 0.2);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            position: relative;
        }

        .capsolver-badge {
            position: absolute;
            top: -10px;
            right: 15px;
            background: var(--primary);
            color: white;
            font-size: 0.7rem;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 20px;
            box-shadow: var(--glow-primary);
        }

        .token-display {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 10px;
            font-family: 'Consolas', monospace;
            color: var(--accent);
            word-break: break-all;
            border: 1px dashed rgba(0, 255, 194, 0.3);
            margin-top: 15px;
            font-size: 0.9rem;
        }

        /* Result Panel & Alerts */
        .alert-custom {
            border-radius: 12px;
            border: none;
            padding: 15px 20px;
            display: none;
            font-weight: 500;
            font-size: 0.9rem;
            animation: slideInUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes slideInUp {
            from {
                transform: translateY(20px);
                opacity: 0;
            }

            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .alert-danger {
            background: rgba(220, 53, 69, 0.1);
            color: #ff6b6b;
            border: 1px solid rgba(220, 53, 69, 0.2);
        }

        .alert-success {
            background: rgba(40, 167, 69, 0.1);
            color: #51cf66;
            border: 1px solid rgba(40, 167, 69, 0.2);
        }

        .alert-info {
            background: rgba(23, 162, 184, 0.1);
            color: #3bc9db;
            border: 1px solid rgba(23, 162, 184, 0.2);
        }

        .alert-warning {
            background: rgba(255, 193, 7, 0.1);
            color: #fcc419;
            border: 1px solid rgba(255, 193, 7, 0.2);
        }

        /* User Info Result Block */
        .user-info-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-glass);
            margin-top: 20px;
            display: none;
            animation: slideInUp 0.4s;
        }

        .user-info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .user-info-item:last-child {
            border-bottom: none;
        }

        .user-info-label {
            color: var(--text-muted);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .user-info-value {
            color: white;
            font-weight: 600;
            font-size: 0.95rem;
        }

        .status-dot {
            height: 10px;
            width: 10px;
            background-color: #43b581;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px #43b581;
            margin-right: 8px;
        }

        .pane-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* Loading Spinner inside Button */
        .spinner-icon {
            animation: spin 1s infinite linear;
        }

        @keyframes spin {
            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-darker);
        }

        ::-webkit-scrollbar-thumb {
            background: #40444b;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #5865F2;
        }

        /* Token Vault */
        .vault-token-box {
            background: rgba(0,0,0,0.5);
            border: 1px dashed rgba(0, 255, 194, 0.35);
            border-radius: 12px;
            padding: 18px 20px;
            font-family: 'Consolas', monospace;
            font-size: 0.82rem;
            color: var(--accent);
            word-break: break-all;
            position: relative;
            min-height: 60px;
        }

        .vault-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .btn-small {
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .btn-copy {
            background: rgba(0, 255, 194, 0.12);
            color: var(--accent);
            border: 1px solid rgba(0,255,194,0.3);
        }
        .btn-copy:hover { background: rgba(0,255,194,0.22); }

        .btn-danger-sm {
            background: rgba(220, 53, 69, 0.12);
            color: #ff6b6b;
            border: 1px solid rgba(220,53,69,0.3);
        }
        .btn-danger-sm:hover { background: rgba(220,53,69,0.22); }

        /* Token Decoder */
        .decode-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 20px;
        }
        @media (max-width: 600px) { .decode-grid { grid-template-columns: 1fr; } }

        .decode-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 16px 18px;
        }

        .decode-card-title {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .decode-card-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: white;
            word-break: break-all;
        }

        .decode-card.accent-card { border-color: rgba(0,255,194,0.25); }
        .decode-card.accent-card .decode-card-value { color: var(--accent); }

        .avatar-preview {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            border: 3px solid var(--primary);
            box-shadow: var(--glow-primary);
            object-fit: cover;
        }

        .nitro-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .nitro-none { background: rgba(255,255,255,0.07); color: var(--text-muted); }
        .nitro-classic { background: rgba(88,101,242,0.2); color: #a6b2ff; }
        .nitro-full { background: rgba(235,69,158,0.2); color: #ff79c6; }

        /* ── Telegram Hub ── */
        :root { --tg: #229ED9; --tg-hover: #1a8bbf; --glow-tg: 0 0 20px rgba(34,158,217,0.35); }

        .tg-sub-nav {
            background: var(--bg-glass-input);
            border-radius: 12px;
            padding: 5px;
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 22px;
        }
        .tg-sub-nav .nav-link {
            flex: 1;
            text-align: center;
            border-radius: 8px;
            padding: 9px 12px;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-muted);
            transition: all 0.2s;
            cursor: pointer;
            border: none;
            background: transparent;
            white-space: nowrap;
        }
        .tg-sub-nav .nav-link.active {
            background: rgba(34,158,217,0.15);
            color: #55c2f5;
            border: 1px solid rgba(34,158,217,0.35);
        }

        .btn-tg {
            background: var(--tg);
            color: white;
            box-shadow: 0 5px 15px rgba(34,158,217,0.3);
        }
        .btn-tg:hover {
            background: var(--tg-hover) !important;
            transform: translateY(-2px);
            box-shadow: var(--glow-tg);
        }

        .tg-info-card {
            background: linear-gradient(135deg, rgba(34,158,217,0.06), rgba(255,255,255,0.01));
            border: 1px solid rgba(34,158,217,0.2);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            display: none;
            animation: slideInUp 0.4s;
        }
        .tg-info-item {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            gap: 12px;
        }
        .tg-info-item:last-child { border-bottom: none; }
        .tg-info-label { color: var(--text-muted); font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.8px; flex-shrink: 0; }
        .tg-info-value { color: white; font-weight: 600; font-size: 0.92rem; text-align: right; word-break: break-all; }
        .tg-dot { height:10px; width:10px; background:#229ED9; border-radius:50%; display:inline-block; box-shadow: 0 0 10px #229ED9; margin-right:8px; }
    </style>
</head>

<body>

    <!-- Dynamic Background Elements -->
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>

    <div class="main-container">

        <!-- LEFT SIDEBAR -->
        <div class="glass-panel nav-wrapper">
            <div>
                <div class="brand"><i class="fa-brands fa-discord"></i> DevThinh</div>
                <div class="brand-subtitle">Bảng Điều Khiển Nâng Cao</div>
            </div>

            <div class="nav flex-column nav-pills-custom" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                <button class="nav-link active" id="v-login-tab" data-bs-toggle="pill" data-bs-target="#v-login"
                    type="button" role="tab" aria-selected="true">
                    <i class="fa-solid fa-right-to-bracket"></i> Đăng Nhập
                </button>
                <button class="nav-link" id="v-check-tab" data-bs-toggle="pill" data-bs-target="#v-check" type="button"
                    role="tab" aria-selected="false">
                    <i class="fa-solid fa-shield-halved"></i> Kiểm Tra Session
                </button>
                <button class="nav-link" id="v-join-tab" data-bs-toggle="pill" data-bs-target="#v-join" type="button"
                    role="tab" aria-selected="false">
                    <i class="fa-solid fa-satellite-dish"></i> Vào Server
                </button>
                <button class="nav-link" id="v-vault-tab" data-bs-toggle="pill" data-bs-target="#v-vault" type="button"
                    role="tab" aria-selected="false">
                    <i class="fa-solid fa-vault"></i> Kho Token
                </button>
                <button class="nav-link" id="v-decode-tab" data-bs-toggle="pill" data-bs-target="#v-decode" type="button"
                    role="tab" aria-selected="false">
                    <i class="fa-solid fa-magnifying-glass-chart"></i> Giải Mã Token
                </button>
                <button class="nav-link" id="v-tg-tab" data-bs-toggle="pill" data-bs-target="#v-tg" type="button"
                    role="tab" aria-selected="false" style="margin-top:4px;">
                    <i class="fa-brands fa-telegram" style="color:#229ED9;"></i> Telegram Hub
                </button>
            </div>

            <div
                style="margin-top: auto; padding-top: 20px; font-size: 0.75rem; color: var(--text-muted); text-align: center;">
                Kết Nối Cục Bộ • v2026.01
            </div>
        </div>

        <!-- RIGHT CONTENT AREA -->
        <div class="glass-panel content-wrapper">
            <div class="tab-content" id="v-pills-tabContent">

                <!-- AUTHENTICATION TAB -->
                <div class="tab-pane fade show active" id="v-login" role="tabpanel" tabindex="0">
                    <h2 class="pane-title"><i class="fa-solid fa-fingerprint text-primary"></i> Truy Cập Hệ Thống</h2>

                    <div class="nav sub-nav mb-4" id="loginType" role="tablist">
                        <button class="nav-link active" id="token-login-tab" data-bs-toggle="pill"
                            data-bs-target="#tokenLogin" type="button" role="tab" aria-selected="true">
                            Token Trực Tiếp
                        </button>
                        <button class="nav-link" id="email-login-tab" data-bs-toggle="pill" data-bs-target="#emailLogin"
                            type="button" role="tab" aria-selected="false">
                            Tài Khoản
                        </button>
                    </div>

                    <div class="tab-content">
                        <!-- Token Auth -->
                        <div class="tab-pane fade show active" id="tokenLogin" role="tabpanel">
                            <div class="mb-4">
                                <label class="form-label">Token Xác Thực</label>
                                <input type="text" class="form-control" id="directToken"
                                    placeholder="Dán Token từ DevTools vào đây...">
                            </div>
                            <button class="btn btn-primary btn-modern" onclick="saveDirectToken()">
                                <i class="fa-solid fa-floppy-disk"></i> Lưu Kết Nối
                            </button>
                        </div>

                        <!-- Credential Auth -->
                        <div class="tab-pane fade" id="emailLogin" role="tabpanel">
                            <div class="row g-3">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Địa Chỉ Email</label>
                                    <div class="input-group">
                                        <span class="input-group-text"
                                            style="background:var(--bg-glass-input); border:1px solid var(--border-glass); border-right:none; color:var(--text-muted);"><i
                                                class="fa-solid fa-envelope"></i></span>
                                        <input type="email" class="form-control" id="email"
                                            placeholder="name@domain.com" style="border-left:none;">
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Mật Khẩu</label>
                                    <div class="input-group">
                                        <span class="input-group-text"
                                            style="background:var(--bg-glass-input); border:1px solid var(--border-glass); border-right:none; color:var(--text-muted);"><i
                                                class="fa-solid fa-lock"></i></span>
                                        <input type="password" class="form-control" id="password" placeholder="••••••••"
                                            style="border-left:none;">
                                    </div>
                                </div>
                            </div>

                            <!-- CapSolver Extension -->
                            <div class="capsolver-group">
                                <span class="capsolver-badge">BETA</span>
                                <label class="form-label" style="color: #a6b2ff;"><i class="fa-solid fa-robot"></i>
                                    CapSolver Tự Động Bypass</label>
                                <input type="text" class="form-control" id="capsolverKey"
                                    placeholder="API Key CapSolver (Tuỳ chọn)">
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 8px;">Tự động
                                    phát hiện lỗi captcha và điều hướng qua trình giải AI.</div>
                            </div>

                            <!-- MFA Hidden Block -->
                            <div class="mb-4" id="mfaGroup" style="display: none;">
                                <label class="form-label text-warning"><i class="fa-solid fa-shield-cat"></i>
                                    Xác Thực Hai Yếu Tố (MFA)</label>
                                <input type="text" class="form-control" id="mfaCode"
                                    placeholder="Nhập mã 6 chữ số từ Authenticator"
                                    style="border-color: #fcc419; box-shadow: 0 0 10px rgba(252, 196, 25, 0.1);">
                                <input type="hidden" id="loginTicket">
                            </div>

                            <button class="btn btn-primary btn-modern" id="btnEmailLogin" onclick="loginEmail()">
                                <i class="fa-solid fa-play"></i> Bắt Đầu Đăng Nhập
                            </button>
                        </div>
                    </div>
                </div>

                <!-- CHECK TOKEN TAB -->
                <div class="tab-pane fade" id="v-check" role="tabpanel" tabindex="0">
                    <h2 class="pane-title"><i class="fa-solid fa-microscope text-primary"></i> Kiểm Tra Session</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 25px;">Xác minh tính hợp lệ
                        của token hoặc kiểm tra session đã lưu.</p>

                    <div class="mb-4">
                        <label class="form-label">Token Cần Kiểm Tra (Để trống để dùng token đã lưu)</label>
                        <input type="text" class="form-control" id="checkToken" placeholder="Dán token vào đây...">
                    </div>

                    <button class="btn btn-primary btn-modern" id="btnCheckToken" onclick="checkUserInfo()">
                        <i class="fa-solid fa-radar"></i> Chạy Kiểm Tra
                    </button>

                    <div class="user-info-card" id="userInfoResult">
                        <h5
                            style="color: white; font-weight: 700; margin-bottom: 20px; font-family: 'Outfit', sans-serif;">
                            <span class="status-dot"></span> Đã Xác Định
                        </h5>
                        <div class="user-info-item">
                            <span class="user-info-label">Tên</span>
                            <span class="user-info-value" id="resUsername"></span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">User ID</span>
                            <span class="user-info-value" id="resId"></span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">Email</span>
                            <span class="user-info-value" id="resEmail"></span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">Số Điện Thoại</span>
                            <span class="user-info-value" id="resPhone"></span>
                        </div>
                    </div>
                </div>

                <!-- JOIN SERVER TAB -->
                <div class="tab-pane fade" id="v-join" role="tabpanel" tabindex="0">
                    <h2 class="pane-title"><i class="fa-solid fa-satellite text-primary"></i> Vào Server Discord</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 25px;">Dùng token đã lưu
                        để tham gia server Discord mục tiêu.</p>

                    <div class="mb-4">
                        <label class="form-label">Link / Mã Mời (Invite Code / URL)</label>
                        <div class="input-group">
                            <span class="input-group-text"
                                style="background:var(--bg-glass-input); border:1px solid var(--border-glass); border-right:none; color:var(--text-muted);">
                                <i class="fa-solid fa-link"></i>
                            </span>
                            <input type="text" class="form-control" id="inviteCode" placeholder="hxyz, discord.gg/..."
                                style="border-left:none;">
                        </div>
                    </div>

                    <button class="btn btn-primary btn-modern" id="btnJoinServer" onclick="joinDiscordServer()">
                        <i class="fa-solid fa-bolt"></i> Tham Gia Server
                    </button>
                </div>

                <!-- TOKEN VAULT TAB -->
                <div class="tab-pane fade" id="v-vault" role="tabpanel" tabindex="0">
                    <h2 class="pane-title"><i class="fa-solid fa-vault text-primary"></i> Kho Token</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 25px;">Quản lý token session
                        đã lưu. Token được lưu ở file tạm trên server.</p>

                    <label class="form-label">Token Đã Lưu</label>
                    <div class="vault-token-box" id="vaultTokenDisplay">
                        <span style="color: var(--text-muted); font-style: italic;">Đang tải kho token...</span>
                    </div>

                    <div class="vault-actions">
                        <button class="btn-small btn-copy" onclick="copyVaultToken()">
                            <i class="fa-solid fa-copy"></i> Sao Chép Token
                        </button>
                        <button class="btn-small" onclick="toggleMask()"
                            style="background:rgba(255,255,255,0.05);color:var(--text-muted);border:1px solid var(--border-glass);">
                            <i class="fa-solid fa-eye" id="maskIcon"></i> Ẩn/Hiện
                        </button>
                        <button class="btn-small btn-danger-sm" onclick="deleteVaultToken()">
                            <i class="fa-solid fa-trash"></i> Xóa Token
                        </button>
                    </div>

                    <div id="vaultAlert" class="alert-custom mt-4"></div>
                </div>

                <!-- TOKEN DECODER TAB -->
                <div class="tab-pane fade" id="v-decode" role="tabpanel" tabindex="0">
                    <h2 class="pane-title"><i class="fa-solid fa-magnifying-glass-chart text-primary"></i> Giải Mã Token</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 25px;">Trích xuất thông tin
                        từ Discord token mà không cần gọi API, hoặc lấy hồ sơ đầy đủ.</p>

                    <div class="mb-3">
                        <label class="form-label">Token Cần Giải Mã (Để trống để dùng token đã lưu)</label>
                        <input type="text" class="form-control" id="decodeToken"
                            placeholder="Dán token hoặc để trống...">
                    </div>

                    <div style="display:flex; gap:10px; flex-wrap:wrap;">
                        <button class="btn btn-primary btn-modern" id="btnDecode" onclick="decodeToken()" style="flex:1;">
                            <i class="fa-solid fa-wand-magic-sparkles"></i> Giải Mã Cục Bộ
                        </button>
                        <button class="btn btn-accent btn-modern" id="btnDecodeAPI" onclick="decodeTokenAPI()" style="flex:1;">
                            <i class="fa-solid fa-cloud-arrow-down"></i> Lấy Hồ Sơ Đầy Đủ
                        </button>
                    </div>

                    <div id="decodeResult" style="display:none; margin-top:20px;">
                        <!-- Local decode section -->
                        <div id="localDecodeSection">
                            <div style="font-size:0.75rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:var(--text-muted); margin-bottom:12px;">
                                <i class="fa-solid fa-microchip"></i> Dữ Liệu Nhúng (Không cần API)
                            </div>
                            <div class="decode-grid">
                                <div class="decode-card accent-card">
                                    <div class="decode-card-title">User ID</div>
                                    <div class="decode-card-value" id="dUserId">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Token Được Tạo Lúc</div>
                                    <div class="decode-card-value" id="dCreatedAt">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Tài Khoản Được Tạo Lúc</div>
                                    <div class="decode-card-value" id="dAccountAge">—</div>
                                </div>
                                <div class="decode-card accent-card">
                                    <div class="decode-card-title">Chữ Ký HMAC</div>
                                    <div class="decode-card-value" id="dHmac" style="font-size:0.75rem;">—</div>
                                </div>
                            </div>
                        </div>

                        <!-- Full API profile section -->
                        <div id="apiDecodeSection" style="display:none; margin-top:24px;">
                            <div style="font-size:0.75rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:var(--text-muted); margin-bottom:12px;">
                                <i class="fa-solid fa-cloud"></i> Hồ Sơ Discord API
                            </div>
                            <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
                                <img id="dAvatar" src="" class="avatar-preview" style="display:none;" alt="Ảnh đại diện">
                                <div>
                                    <div style="font-size:1.2rem; font-weight:700; color:white;" id="dUsername">—</div>
                                    <div style="font-size:0.85rem; color:var(--text-muted);" id="dDiscriminator"></div>
                                </div>
                            </div>
                            <div class="decode-grid">
                                <div class="decode-card">
                                    <div class="decode-card-title">Email</div>
                                    <div class="decode-card-value" id="dEmail">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Điện Thoại</div>
                                    <div class="decode-card-value" id="dPhone">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Ngôn Ngữ</div>
                                    <div class="decode-card-value" id="dLocale">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Bảo Mật 2 Lớp</div>
                                    <div class="decode-card-value" id="dMfa">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Email Đã Xác Minh</div>
                                    <div class="decode-card-value" id="dVerified">—</div>
                                </div>
                                <div class="decode-card">
                                    <div class="decode-card-title">Cờ Tài Khoản</div>
                                    <div class="decode-card-value" id="dFlags">—</div>
                                </div>
                                <div class="decode-card" style="grid-column: span 2;">
                                    <div class="decode-card-title">Loại Nitro</div>
                                    <div class="decode-card-value" id="dNitro">—</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="decodeAlert" class="alert-custom mt-4"></div>
                </div>

            </div>

                <!-- TELEGRAM HUB TAB -->
                <div class="tab-pane fade" id="v-tg" role="tabpanel" tabindex="0">
                    <h2 class="pane-title"><i class="fa-brands fa-telegram" style="color:#229ED9;"></i> Telegram Hub</h2>
                    <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:22px;">Tương tác với Telegram Bot API. Nhập Bot Token của bạn để bắt đầu.</p>

                    <!-- Bot Token field (shared) -->
                    <div class="mb-3">
                        <label class="form-label"><i class="fa-solid fa-key" style="color:#229ED9;"></i> &nbsp;Bot Token</label>
                        <input type="text" class="form-control" id="tgBotToken"
                            placeholder="1234567890:ABCDefGhIJKlmNoPQRsTUVwxyZ"
                            style="border-color:rgba(34,158,217,0.3); font-family:'Consolas',monospace; font-size:0.88rem;">
                    </div>

                    <!-- Sub-nav -->
                    <div class="tg-sub-nav" id="tgSubNav" role="tablist">
                        <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#tgBotInfo" type="button"><i class="fa-solid fa-robot"></i> Thông Tin Bot</button>
                        <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tgSendMsg" type="button"><i class="fa-solid fa-paper-plane"></i> Gửi Tin Nhắn</button>
                        <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tgUserLookup" type="button"><i class="fa-solid fa-user-magnifying-glass"></i> Tra Cứu User</button>
                        <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tgChatInfo" type="button"><i class="fa-solid fa-comments"></i> Thông Tin Chat</button>
                    </div>

                    <div class="tab-content">

                        <!-- BOT INFO -->
                        <div class="tab-pane fade show active" id="tgBotInfo" role="tabpanel">
                            <button class="btn btn-tg btn-modern" id="btnTgBotInfo" onclick="tgGetBotInfo()">
                                <i class="fa-solid fa-robot"></i> Lấy Thông Tin Bot
                            </button>
                            <div class="tg-info-card" id="tgBotInfoResult">
                                <h5 style="color:white; font-weight:700; margin-bottom:16px;">
                                    <span class="tg-dot"></span> Bot Đã Xác Định
                                </h5>
                                <div class="tg-info-item"><span class="tg-info-label">Tên</span><span class="tg-info-value" id="tgBotName">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Username</span><span class="tg-info-value" id="tgBotUsername">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Bot ID</span><span class="tg-info-value" id="tgBotId">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Vào Nhóm Được</span><span class="tg-info-value" id="tgBotJoinGroups">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Inline Queries</span><span class="tg-info-value" id="tgBotInline">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Đọc Tất Cả Tin</span><span class="tg-info-value" id="tgBotAllMsg">—</span></div>
                            </div>
                        </div>

                        <!-- SEND MESSAGE -->
                        <div class="tab-pane fade" id="tgSendMsg" role="tabpanel">
                            <div class="mb-3">
                                <label class="form-label">Chat ID / @username</label>
                                <input type="text" class="form-control" id="tgSendChatId" placeholder="-100123456789 or @channelusername">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Nội Dung Tin Nhắn</label>
                                <textarea class="form-control" id="tgSendText" rows="4"
                                    placeholder="Nhập nội dung tin nhắn tại đây..."
                                    style="resize:vertical;"></textarea>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Chế Độ Parse</label>
                                <select class="form-control" id="tgParseMode">
                                    <option value="">Không (văn bản thường)</option>
                                    <option value="Markdown">Markdown</option>
                                    <option value="HTML">HTML</option>
                                </select>
                            </div>
                            <button class="btn btn-tg btn-modern" id="btnTgSend" onclick="tgSendMessage()">
                                <i class="fa-solid fa-paper-plane"></i> Gửi Tin Nhắn
                            </button>
                        </div>

                        <!-- USER LOOKUP -->
                        <div class="tab-pane fade" id="tgUserLookup" role="tabpanel">
                            <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom:16px;">
                                <i class="fa-solid fa-circle-info"></i>
                                Bot chỉ tra cứu được user đã nhắn tin với bot hoặc có nhóm chung.
                            </p>
                            <div class="mb-3">
                                <label class="form-label">User ID</label>
                                <input type="text" class="form-control" id="tgUserId" placeholder="123456789">
                            </div>
                            <button class="btn btn-tg btn-modern" id="btnTgUser" onclick="tgUserLookup()">
                                <i class="fa-solid fa-user-magnifying-glass"></i> Tra Cứu User
                            </button>
                            <div class="tg-info-card" id="tgUserResult">
                                <h5 style="color:white; font-weight:700; margin-bottom:16px;"><span class="tg-dot"></span> Đã Tìm Thấy User</h5>
                                <div class="tg-info-item"><span class="tg-info-label">Họ Tên</span><span class="tg-info-value" id="tgUserName">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Username</span><span class="tg-info-value" id="tgUserUsername">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">User ID</span><span class="tg-info-value" id="tgUserIdResult">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Loại</span><span class="tg-info-value" id="tgUserType">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Là Bot</span><span class="tg-info-value" id="tgUserIsBot">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Ngôn Ngữ</span><span class="tg-info-value" id="tgUserLang">—</span></div>
                            </div>
                        </div>

                        <!-- CHAT INFO -->
                        <div class="tab-pane fade" id="tgChatInfo" role="tabpanel">
                            <div class="mb-3">
                                <label class="form-label">Chat ID / @username</label>
                                <input type="text" class="form-control" id="tgChatId" placeholder="-100123456789 or @groupusername">
                            </div>
                            <button class="btn btn-tg btn-modern" id="btnTgChat" onclick="tgGetChatInfo()">
                                <i class="fa-solid fa-comments"></i> Lấy Thông Tin Chat
                            </button>
                            <div class="tg-info-card" id="tgChatResult">
                                <h5 style="color:white; font-weight:700; margin-bottom:16px;"><span class="tg-dot"></span> Đã Xác Định Chat</h5>
                                <div class="tg-info-item"><span class="tg-info-label">Tiêu Đề</span><span class="tg-info-value" id="tgChatTitle">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Chat ID</span><span class="tg-info-value" id="tgChatIdResult">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Loại</span><span class="tg-info-value" id="tgChatType">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Username</span><span class="tg-info-value" id="tgChatUsername">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Thành Viên</span><span class="tg-info-value" id="tgChatMembers">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Mô Tả</span><span class="tg-info-value" id="tgChatDesc">—</span></div>
                                <div class="tg-info-item"><span class="tg-info-label">Link Mời</span><span class="tg-info-value" id="tgChatInvite">—</span></div>
                            </div>
                        </div>

                    </div><!-- end tab-content -->

                    <div id="tgAlert" class="alert-custom mt-4"></div>
                </div><!-- end v-tg -->

            <!-- GLOBAL RESULT ALERTS -->
            <div id="resultAlert" class="alert-custom mt-4"></div>

        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // System UI Helper
        const AlertSystem = {
            box: document.getElementById("resultAlert"),
            show: function (msg, type, iconClass) {
                this.box.style.display = "block";
                this.box.className = `alert-custom alert-${type} mt-4`;

                let icon = '';
                if (iconClass) icon = `<i class="${iconClass}" style="margin-right: 8px;"></i>`;
                else if (type === 'success') icon = `<i class="fa-solid fa-circle-check" style="margin-right: 8px;"></i>`;
                else if (type === 'danger') icon = `<i class="fa-solid fa-triangle-exclamation" style="margin-right: 8px;"></i>`;
                else if (type === 'warning') icon = `<i class="fa-solid fa-shield-halved" style="margin-right: 8px;"></i>`;
                else if (type === 'info') icon = `<i class="fa-solid fa-circle-info" style="margin-right: 8px;"></i>`;

                this.box.innerHTML = `${icon} ${msg}`;

                // smooth intro
                this.box.style.animation = 'none';
                this.box.offsetHeight; // trigger reflow
                this.box.style.animation = null;
            },
            hide: function () {
                this.box.style.display = "none";
            }
        };

        function resetBtn(btnId, originalText, originalIcon) {
            const btn = document.getElementById(btnId);
            btn.disabled = false;
            btn.innerHTML = `<i class="${originalIcon}"></i> ${originalText}`;
        }

        function loadBtn(btnId, loadingText) {
            const btn = document.getElementById(btnId);
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-circle-notch spinner-icon"></i> ${loadingText}`;
        }

        // Module: Direct Token
        async function saveDirectToken() {
            const token = document.getElementById("directToken").value.trim();
            if (!token) return AlertSystem.show("Please inject a valid token string first.", "danger");

            try {
                const res = await axios.post("/api/save_token", { token: token });
                if (res.data.success) {
                    AlertSystem.show(`Session secured locally.<br><div class="token-display">${token}</div>`, "success");
                } else {
                    AlertSystem.show(res.data.message, "danger");
                }
            } catch (e) {
                AlertSystem.show("Gateway Error: " + (e.response?.data?.message || e.message), "danger");
            }
        }

        // Module: Credential Auth
        async function loginEmail() {
            const email = document.getElementById("email").value.trim();
            const pwd = document.getElementById("password").value.trim();
            const capsolver = document.getElementById("capsolverKey").value.trim();

            const mfaGroup = document.getElementById("mfaGroup");
            const mfaCode = document.getElementById("mfaCode").value.trim();
            const ticket = document.getElementById("loginTicket").value;

            if (!email || !pwd) return AlertSystem.show("Credentials incomplete.", "danger");

            loadBtn("btnEmailLogin", "Establishing Connection...");
            AlertSystem.show("Transmitting payload to Discord API... Awaiting handshake.", "info");

            try {
                const payload = { email: email, password: pwd, capsolver_key: capsolver };

                // MFA Check
                if (mfaGroup.style.display === "block" && mfaCode && ticket) {
                    payload.mfa_code = mfaCode;
                    payload.ticket = ticket;
                    AlertSystem.show("Verifying MFA Integrity...", "info");
                }

                const res = await axios.post("/api/login_email", payload);

                if (res.data.success) {
                    AlertSystem.show(`Connection Authorized.<br><div class="token-display">${res.data.token}</div>`, "success");
                    mfaGroup.style.display = "none";
                    document.getElementById("directToken").value = res.data.token;
                } else if (res.data.require_mfa) {
                    AlertSystem.show("MFA Shield Active. Awaiting secondary code.", "warning");
                    mfaGroup.style.display = "block";
                    document.getElementById("loginTicket").value = res.data.ticket;
                    document.getElementById("mfaCode").focus();
                } else {
                    AlertSystem.show("Authorization Denied: " + res.data.message, "danger");
                }

            } catch (e) {
                AlertSystem.show("Local Server Error: " + (e.response?.data?.message || e.message), "danger");
            } finally {
                resetBtn("btnEmailLogin", "Initiate Login Sequence", "fa-solid fa-play");
            }
        }

        // Module: Session Diagnostics
        async function checkUserInfo() {
            const token = document.getElementById("checkToken").value.trim();
            document.getElementById("userInfoResult").style.display = "none";

            loadBtn("btnCheckToken", "Running Diagnostics...");
            AlertSystem.show("Scanning payload signatures...", "info");

            try {
                const payload = token ? { token: token } : {};
                const res = await axios.post("/api/check", payload);

                if (res.data.success) {
                    document.getElementById("userInfoResult").style.display = "block";
                    const u = res.data.user;
                    document.getElementById("resUsername").innerText = u.username || 'CLASSIFIED';
                    document.getElementById("resId").innerText = u.id || 'CLASSIFIED';
                    document.getElementById("resEmail").innerText = u.email || 'CLASSIFIED';
                    document.getElementById("resPhone").innerText = u.phone || 'NONE';

                    AlertSystem.show("Token Signature Verified and Alive.", "success");
                } else {
                    AlertSystem.show("Token is dead or invalid. Access Revoked.", "danger");
                }
            } catch (e) {
                AlertSystem.show("Diagnostics Failed: " + (e.response?.data?.message || e.message), "danger", "fa-solid fa-heart-crack");
            } finally {
                resetBtn("btnCheckToken", "Run Diagnostics", "fa-solid fa-radar");
            }
        }

        // Module: Guild Infiltration
        async function joinDiscordServer() {
            const invite = document.getElementById("inviteCode").value.trim();
            const token = document.getElementById("checkToken").value.trim();
            if (!invite) return AlertSystem.show("Input target coordinate (Invite code).", "danger");

            loadBtn("btnJoinServer", "Executing Injection...");
            AlertSystem.show("Transmitting join payload...", "info");

            try {
                const payload = { invite: invite };
                if (token) payload.token = token;

                const res = await axios.post("/api/join", payload);

                if (res.data.success) {
                    AlertSystem.show(`Successfully breached Guild Server: <b style="color:white; margin-left: 5px;">${res.data.guild_name}</b>`, "success");
                } else {
                    AlertSystem.show("Target unreachable: " + res.data.message, "danger");
                }
            } catch (e) {
                AlertSystem.show("Injection Failed: " + (e.response?.data?.message || e.message), "danger");
            } finally {
                resetBtn("btnJoinServer", "Execute Injection", "fa-solid fa-bolt");
            }
        }

        // =====================================================
        // MODULE: TOKEN VAULT
        // =====================================================
        let _vaultToken = null;
        let _vaultMasked = true;

        function showVaultAlert(msg, type) {
            const el = document.getElementById('vaultAlert');
            el.style.display = 'block';
            el.className = `alert-custom alert-${type} mt-4`;
            el.innerHTML = msg;
        }

        function renderVaultDisplay() {
            const box = document.getElementById('vaultTokenDisplay');
            if (!_vaultToken) {
                box.innerHTML = '<span style="color:var(--text-muted); font-style:italic;">No token stored in vault.</span>';
                return;
            }
            if (_vaultMasked) {
                const parts = _vaultToken.split('.');
                const masked = parts.map((p, i) => i === 0 ? p : '●'.repeat(Math.min(p.length, 12))).join('.');
                box.innerHTML = `<span style="color:var(--accent);">${masked}</span> <span style="color:var(--text-muted); font-size:0.75rem; margin-left:8px;">(masked)</span>`;
            } else {
                box.innerHTML = `<span style="color:var(--accent);">${_vaultToken}</span>`;
            }
        }

        async function loadVault() {
            try {
                const res = await axios.get('/api/get_token');
                _vaultToken = res.data.token || null;
                renderVaultDisplay();
            } catch {
                document.getElementById('vaultTokenDisplay').innerHTML =
                    '<span style="color:#ff6b6b;">Failed to load vault.</span>';
            }
        }

        function toggleMask() {
            _vaultMasked = !_vaultMasked;
            const icon = document.getElementById('maskIcon');
            icon.className = _vaultMasked ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash';
            renderVaultDisplay();
        }

        async function copyVaultToken() {
            if (!_vaultToken) return showVaultAlert('No token to copy.', 'danger');
            await navigator.clipboard.writeText(_vaultToken);
            showVaultAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Token copied to clipboard!', 'success');
        }

        async function deleteVaultToken() {
            if (!_vaultToken) return showVaultAlert('Vault is already empty.', 'warning');
            if (!confirm('Are you sure you want to delete the saved token?')) return;
            try {
                const res = await axios.delete('/api/delete_token');
                if (res.data.success) {
                    _vaultToken = null;
                    renderVaultDisplay();
                    showVaultAlert('<i class="fa-solid fa-trash" style="margin-right:6px;"></i> Token deleted from vault.', 'success');
                }
            } catch (e) {
                showVaultAlert('Delete failed: ' + (e.response?.data?.message || e.message), 'danger');
            }
        }

        // Load vault when that tab is shown
        document.getElementById('v-vault-tab').addEventListener('shown.bs.tab', loadVault);

        // =====================================================
        // MODULE: TELEGRAM HUB
        // =====================================================
        function tgShowAlert(msg, type) {
            const el = document.getElementById('tgAlert');
            el.style.display = 'block';
            el.className = `alert-custom alert-${type} mt-4`;
            el.innerHTML = msg;
        }
        function tgHideAlert() { document.getElementById('tgAlert').style.display = 'none'; }

        function getBotToken() {
            const t = document.getElementById('tgBotToken').value.trim();
            if (!t) tgShowAlert('<i class="fa-solid fa-triangle-exclamation" style="margin-right:6px;"></i> Please enter a Bot Token first.', 'danger');
            return t;
        }

        // --- Bot Info ---
        async function tgGetBotInfo() {
            const token = getBotToken(); if (!token) return;
            tgHideAlert();
            loadBtn('btnTgBotInfo', 'Fetching...');
            try {
                const res = await axios.post('/api/tg/bot_info', { bot_token: token });
                if (!res.data.success) { tgShowAlert('Error: ' + res.data.message, 'danger'); return; }
                const b = res.data.bot;
                document.getElementById('tgBotName').innerText = b.first_name || '—';
                document.getElementById('tgBotUsername').innerText = b.username ? '@' + b.username : '—';
                document.getElementById('tgBotId').innerText = b.id || '—';
                document.getElementById('tgBotJoinGroups').innerText = b.can_join_groups ? '✅ Yes' : '❌ No';
                document.getElementById('tgBotInline').innerText = b.supports_inline_queries ? '✅ Yes' : '❌ No';
                document.getElementById('tgBotAllMsg').innerText = b.can_read_all_group_messages ? '✅ Yes' : '❌ No';
                document.getElementById('tgBotInfoResult').style.display = 'block';
                tgShowAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Bot token valid — info loaded.', 'success');
            } catch(e) {
                tgShowAlert('Request failed: ' + (e.response?.data?.message || e.message), 'danger');
            } finally { resetBtn('btnTgBotInfo', 'Get Bot Info', 'fa-solid fa-robot'); }
        }

        // --- Send Message ---
        async function tgSendMessage() {
            const token = getBotToken(); if (!token) return;
            const chatId = document.getElementById('tgSendChatId').value.trim();
            const text = document.getElementById('tgSendText').value.trim();
            const parseMode = document.getElementById('tgParseMode').value;
            if (!chatId) return tgShowAlert('Please enter a Chat ID or @username.', 'danger');
            if (!text) return tgShowAlert('Message text cannot be empty.', 'danger');
            tgHideAlert();
            loadBtn('btnTgSend', 'Sending...');
            try {
                const payload = { bot_token: token, chat_id: chatId, text: text };
                if (parseMode) payload.parse_mode = parseMode;
                const res = await axios.post('/api/tg/send_message', payload);
                if (res.data.success) {
                    tgShowAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Message sent successfully!', 'success');
                    document.getElementById('tgSendText').value = '';
                } else {
                    tgShowAlert('Failed: ' + res.data.message, 'danger');
                }
            } catch(e) {
                tgShowAlert('Request failed: ' + (e.response?.data?.message || e.message), 'danger');
            } finally { resetBtn('btnTgSend', 'Send Message', 'fa-solid fa-paper-plane'); }
        }

        // --- User Lookup ---
        async function tgUserLookup() {
            const token = getBotToken(); if (!token) return;
            const userId = document.getElementById('tgUserId').value.trim();
            if (!userId) return tgShowAlert('Please enter a User ID.', 'danger');
            tgHideAlert();
            loadBtn('btnTgUser', 'Looking up...');
            try {
                const res = await axios.post('/api/tg/get_user', { bot_token: token, user_id: userId });
                if (!res.data.success) { tgShowAlert('Error: ' + res.data.message, 'danger'); return; }
                const u = res.data.user;
                const fullName = [u.first_name, u.last_name].filter(Boolean).join(' ');
                document.getElementById('tgUserName').innerText = fullName || '—';
                document.getElementById('tgUserUsername').innerText = u.username ? '@' + u.username : 'None';
                document.getElementById('tgUserIdResult').innerText = u.id || '—';
                document.getElementById('tgUserType').innerText = u.type || '—';
                document.getElementById('tgUserIsBot').innerText = u.is_bot ? '🤖 Yes' : '👤 No';
                document.getElementById('tgUserLang').innerText = u.language_code || 'Unknown';
                document.getElementById('tgUserResult').style.display = 'block';
                tgShowAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> User info retrieved.', 'success');
            } catch(e) {
                tgShowAlert('Request failed: ' + (e.response?.data?.message || e.message), 'danger');
            } finally { resetBtn('btnTgUser', 'Lookup User', 'fa-solid fa-user-magnifying-glass'); }
        }

        // --- Chat Info ---
        async function tgGetChatInfo() {
            const token = getBotToken(); if (!token) return;
            const chatId = document.getElementById('tgChatId').value.trim();
            if (!chatId) return tgShowAlert('Please enter a Chat ID or @username.', 'danger');
            tgHideAlert();
            loadBtn('btnTgChat', 'Fetching...');
            try {
                const res = await axios.post('/api/tg/get_chat', { bot_token: token, chat_id: chatId });
                if (!res.data.success) { tgShowAlert('Error: ' + res.data.message, 'danger'); return; }
                const c = res.data.chat;
                document.getElementById('tgChatTitle').innerText = c.title || c.first_name || '—';
                document.getElementById('tgChatIdResult').innerText = c.id || '—';
                document.getElementById('tgChatType').innerText = c.type || '—';
                document.getElementById('tgChatUsername').innerText = c.username ? '@' + c.username : 'None';
                document.getElementById('tgChatMembers').innerText = res.data.member_count !== null ? res.data.member_count.toLocaleString() : 'N/A';
                document.getElementById('tgChatDesc').innerText = c.description || 'No description';
                document.getElementById('tgChatInvite').innerText = c.invite_link || 'None';
                document.getElementById('tgChatResult').style.display = 'block';
                tgShowAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Chat info loaded.', 'success');
            } catch(e) {
                tgShowAlert('Request failed: ' + (e.response?.data?.message || e.message), 'danger');
            } finally { resetBtn('btnTgChat', 'Get Chat Info', 'fa-solid fa-comments'); }
        }

        // =====================================================
        // MODULE: TOKEN DECODER
        // =====================================================
        const DISCORD_EPOCH = 1420070400000n;

        function showDecodeAlert(msg, type) {
            const el = document.getElementById('decodeAlert');
            el.style.display = 'block';
            el.className = `alert-custom alert-${type} mt-4`;
            el.innerHTML = msg;
        }
        function hideDecodeAlert() { document.getElementById('decodeAlert').style.display = 'none'; }

        function base64UrlDecode(str) {
            str = str.replace(/-/g, '+').replace(/_/g, '/');
            while (str.length % 4) str += '=';
            return atob(str);
        }

        function decodeLocalToken(tokenStr) {
            const parts = tokenStr.split('.');
            if (parts.length !== 3) return null;

            // Part 1: base64 encoded user ID
            let userId;
            try {
                userId = atob(parts[0]);
            } catch { userId = base64UrlDecode(parts[0]); }

            // Part 2: base64 encoded timestamp (seconds since epoch)
            let tokenTs = null;
            try {
                const raw = base64UrlDecode(parts[1]);
                // If the decoded string is a number string
                const asInt = parseInt(raw, 10);
                if (!isNaN(asInt)) {
                    tokenTs = new Date(asInt * 1000);
                } else {
                    // Try reading as 4-byte big-endian int
                    const bytes = Array.from(raw).map(c => c.charCodeAt(0));
                    if (bytes.length >= 4) {
                        const val = (bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | bytes[3];
                        tokenTs = new Date(val * 1000);
                    }
                }
            } catch {}

            // Account creation from User ID (Discord Snowflake)
            let accountCreated = null;
            try {
                const snowflake = BigInt(userId.trim());
                const tsBig = (snowflake >> 22n) + DISCORD_EPOCH;
                accountCreated = new Date(Number(tsBig));
            } catch {}

            return {
                userId: userId.trim(),
                hmac: parts[2],
                tokenCreated: tokenTs ? tokenTs.toUTCString() : 'Unable to decode',
                accountCreated: accountCreated ? accountCreated.toUTCString() : 'Unable to decode'
            };
        }

        async function getTokenForDecode() {
            let t = document.getElementById('decodeToken').value.trim();
            if (!t) {
                const res = await axios.get('/api/get_token');
                t = res.data.token;
            }
            return t;
        }

        async function decodeToken() {
            hideDecodeAlert();
            let tokenStr;
            try { tokenStr = await getTokenForDecode(); } catch { return showDecodeAlert('Could not retrieve token.', 'danger'); }
            if (!tokenStr) return showDecodeAlert('No token provided or stored.', 'danger');

            const info = decodeLocalToken(tokenStr);
            if (!info) return showDecodeAlert('Invalid token format. Must be 3-part dot-separated.', 'danger');

            document.getElementById('dUserId').innerText = info.userId;
            document.getElementById('dCreatedAt').innerText = info.tokenCreated;
            document.getElementById('dAccountAge').innerText = info.accountCreated;
            document.getElementById('dHmac').innerText = info.hmac;

            document.getElementById('apiDecodeSection').style.display = 'none';
            document.getElementById('decodeResult').style.display = 'block';
            showDecodeAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Token decoded locally — no API call made.', 'success');
        }

        const NITRO_MAP = { 0: 'None', 1: 'Nitro Classic', 2: 'Nitro Full', 3: 'Nitro Basic' };

        async function decodeTokenAPI() {
            hideDecodeAlert();
            let tokenStr;
            try { tokenStr = await getTokenForDecode(); } catch { return showDecodeAlert('Could not retrieve token.', 'danger'); }
            if (!tokenStr) return showDecodeAlert('No token provided or stored.', 'danger');

            loadBtn('btnDecodeAPI', 'Fetching Profile...');

            try {
                const res = await axios.post('/api/decode', { token: tokenStr });
                if (!res.data.success) {
                    showDecodeAlert('API Error: ' + res.data.message, 'danger');
                    return;
                }

                const u = res.data.user;
                const local = decodeLocalToken(tokenStr);

                // Local section
                if (local) {
                    document.getElementById('dUserId').innerText = local.userId;
                    document.getElementById('dCreatedAt').innerText = local.tokenCreated;
                    document.getElementById('dAccountAge').innerText = local.accountCreated;
                    document.getElementById('dHmac').innerText = local.hmac;
                }

                // API profile section
                document.getElementById('dUsername').innerText = u.global_name || u.username || '—';
                document.getElementById('dDiscriminator').innerText =
                    u.discriminator && u.discriminator !== '0' ? `#${u.discriminator}` : `@${u.username}`;
                document.getElementById('dEmail').innerText = u.email || 'Not available';
                document.getElementById('dPhone').innerText = u.phone || 'None';
                document.getElementById('dLocale').innerText = u.locale || '—';
                document.getElementById('dMfa').innerText = u.mfa_enabled ? '✅ Enabled' : '❌ Disabled';
                document.getElementById('dVerified').innerText = u.verified ? '✅ Verified' : '❌ Not Verified';
                document.getElementById('dFlags').innerText = u.public_flags !== undefined ? `${u.public_flags}` : '—';

                const nitroLabel = NITRO_MAP[u.premium_type || 0] || 'Unknown';
                const nClass = u.premium_type === 2 ? 'nitro-full' : u.premium_type === 1 ? 'nitro-classic' : 'nitro-none';
                document.getElementById('dNitro').innerHTML = `<span class="nitro-badge ${nClass}">${nitroLabel}</span>`;

                // Avatar
                const avatarEl = document.getElementById('dAvatar');
                if (u.avatar) {
                    avatarEl.src = `https://cdn.discordapp.com/avatars/${u.id}/${u.avatar}.webp?size=128`;
                    avatarEl.style.display = 'block';
                } else {
                    avatarEl.style.display = 'none';
                }

                document.getElementById('apiDecodeSection').style.display = 'block';
                document.getElementById('decodeResult').style.display = 'block';
                showDecodeAlert('<i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Full profile extracted successfully.', 'success');

            } catch (e) {
                showDecodeAlert('Request failed: ' + (e.response?.data?.message || e.message), 'danger');
            } finally {
                resetBtn('btnDecodeAPI', 'Fetch Full Profile', 'fa-solid fa-cloud-arrow-down');
            }
        }
    </script>

</body>

</html>
"""

app = Flask(__name__)

GLOBAL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

TOKEN_FILE = "/tmp/token.txt"

def load_saved_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def capsolver_solve(site_key, site_url, capsolver_key):
    try:
        payload = {
            "clientKey": capsolver_key,
            "task": {
                "type": "HCaptchaTaskProxyLess",
                "websiteURL": site_url,
                "websiteKey": site_key
            }
        }
        res = requests.post("https://api.capsolver.com/createTask", json=payload)
        res_data = res.json()
        if res_data.get("errorId") == 0:
            task_id = res_data.get("taskId")
            for _ in range(30):
                time.sleep(2)
                check_res = requests.post("https://api.capsolver.com/getTaskResult", json={
                    "clientKey": capsolver_key,
                    "taskId": task_id
                })
                check_data = check_res.json()
                if check_data.get("status") == "ready":
                    return {"success": True, "token": check_data.get("solution", {}).get("gRecaptchaResponse")}
                elif check_data.get("status") == "failed":
                    return {"success": False, "message": check_data.get("errorDescription")}
            return {"success": False, "message": "Captcha solving timed out"}
        else:
            return {"success": False, "message": res_data.get("errorDescription", "Unknown error creating task")}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/save_token", methods=["POST"])
def api_save_token():
    data = request.json
    token = data.get("token")
    if token:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "No token provided."}), 400

@app.route("/api/get_token", methods=["GET"])
def api_get_token():
    token = load_saved_token()
    if token:
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False, "token": None, "message": "No token stored."})

@app.route("/api/delete_token", methods=["DELETE"])
def api_delete_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "No token file found."}), 404

@app.route("/api/decode", methods=["POST"])
def api_decode():
    data = request.json or {}
    token = data.get("token") or load_saved_token()
    if not token:
        return jsonify({"success": False, "message": "No token provided or stored."}), 400
    headers = GLOBAL_HEADERS.copy()
    headers["Authorization"] = token
    res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if res.status_code == 200:
        return jsonify({"success": True, "user": res.json()})
    return jsonify({"success": False, "message": f"Token invalid or expired. ({res.status_code})"}), 401

@app.route("/api/login_email", methods=["POST"])
def api_login_email():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    capsolver_key = data.get("capsolver_key", "").strip()
    mfa_code = data.get("mfa_code")
    ticket = data.get("ticket")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password."}), 400

    payload = {"login": email, "password": password}
    
    if mfa_code and ticket:
        mfa_payload = {"code": mfa_code, "ticket": ticket, "login_source": None, "gift_code_sku_id": None}
        mfa_url = "https://discord.com/api/v9/auth/mfa/totp"
        res = requests.post(mfa_url, json=mfa_payload, headers=GLOBAL_HEADERS)
        if res.status_code == 200:
            token = res.json().get("token")
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            return jsonify({"success": True, "token": token})
        else:
            return jsonify({"success": False, "message": f"MFA Failed: {res.text}"}), 400

    # Normal login
    res = requests.post("https://discord.com/api/v9/auth/login", json=payload, headers=GLOBAL_HEADERS)
    
    # CapSolver Handle
    if res.status_code == 400 and "captcha" in res.text.lower():
        if capsolver_key:
            captcha_sitekey = res.json().get("captcha_sitekey")
            if captcha_sitekey:
                cap_result = capsolver_solve(captcha_sitekey, "https://discord.com/login", capsolver_key)
                if cap_result["success"]:
                    payload["captcha_key"] = cap_result["token"]
                    # Retry
                    res = requests.post("https://discord.com/api/v9/auth/login", json=payload, headers=GLOBAL_HEADERS)
                else:
                    return jsonify({"success": False, "message": "CapSolver Failed: " + cap_result["message"]}), 400
        else:
            return jsonify({"success": False, "message": "Captcha required but no CapSolver key provided."}), 400

    data_res = res.json()
    if "token" in data_res:
        token = data_res["token"]
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        return jsonify({"success": True, "token": token})
    elif "mfa" in res.text.lower() or "ticket" in data_res:
        return jsonify({"success": False, "require_mfa": True, "ticket": data_res.get("ticket")})
    else:
        return jsonify({"success": False, "message": res.text}), 400

@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.json or {}
    token = data.get("token") or load_saved_token()
    if not token:
        return jsonify({"success": False, "message": "No token available."}), 400
    
    headers = GLOBAL_HEADERS.copy()
    headers["Authorization"] = token
    res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if res.status_code == 200:
        return jsonify({"success": True, "user": res.json()})
    else:
        return jsonify({"success": False, "message": "Invalid or expired token."}), 401

@app.route("/api/join", methods=["POST"])
def api_join():
    data = request.json
    invite = data.get("invite", "").strip()
    invite_code = invite.split("/")[-1]
    
    token = data.get("token") or load_saved_token()
    if not token:
        return jsonify({"success": False, "message": "No token available."}), 400
    
    headers = GLOBAL_HEADERS.copy()
    headers["Authorization"] = token
    
    res = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers, json={})
    if res.status_code == 200:
        guild = res.json().get("guild", {})
        return jsonify({"success": True, "guild_name": guild.get("name", "Unknown Server")})
    else:
        return jsonify({"success": False, "message": res.text}), 400

# ─────────── TELEGRAM HUB ───────────

TG_BASE = "https://api.telegram.org/bot{token}/{method}"

def tg_call(bot_token, method, payload=None):
    url = TG_BASE.format(token=bot_token, method=method)
    res = requests.post(url, json=payload or {}, timeout=10)
    return res.json()

@app.route("/api/tg/bot_info", methods=["POST"])
def api_tg_bot_info():
    data = request.json or {}
    bot_token = data.get("bot_token", "").strip()
    if not bot_token:
        return jsonify({"success": False, "message": "Bot token required."}), 400
    result = tg_call(bot_token, "getMe")
    if result.get("ok"):
        return jsonify({"success": True, "bot": result["result"]})
    return jsonify({"success": False, "message": result.get("description", "Unknown error")}), 400

@app.route("/api/tg/send_message", methods=["POST"])
def api_tg_send_message():
    data = request.json or {}
    bot_token = data.get("bot_token", "").strip()
    chat_id = data.get("chat_id", "").strip()
    text = data.get("text", "").strip()
    parse_mode = data.get("parse_mode", "")
    if not bot_token or not chat_id or not text:
        return jsonify({"success": False, "message": "bot_token, chat_id, and text are required."}), 400
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    result = tg_call(bot_token, "sendMessage", payload)
    if result.get("ok"):
        return jsonify({"success": True, "message_id": result["result"].get("message_id")})
    return jsonify({"success": False, "message": result.get("description", "Unknown error")}), 400

@app.route("/api/tg/get_user", methods=["POST"])
def api_tg_get_user():
    data = request.json or {}
    bot_token = data.get("bot_token", "").strip()
    user_id = data.get("user_id", "").strip()
    if not bot_token or not user_id:
        return jsonify({"success": False, "message": "bot_token and user_id are required."}), 400
    result = tg_call(bot_token, "getChat", {"chat_id": user_id})
    if result.get("ok"):
        return jsonify({"success": True, "user": result["result"]})
    return jsonify({"success": False, "message": result.get("description", "Unknown error")}), 400

@app.route("/api/tg/get_chat", methods=["POST"])
def api_tg_get_chat():
    data = request.json or {}
    bot_token = data.get("bot_token", "").strip()
    chat_id = data.get("chat_id", "").strip()
    if not bot_token or not chat_id:
        return jsonify({"success": False, "message": "bot_token and chat_id are required."}), 400
    chat_result = tg_call(bot_token, "getChat", {"chat_id": chat_id})
    if not chat_result.get("ok"):
        return jsonify({"success": False, "message": chat_result.get("description", "Unknown error")}), 400
    member_count = None
    count_result = tg_call(bot_token, "getChatMemberCount", {"chat_id": chat_id})
    if count_result.get("ok"):
        member_count = count_result["result"]
    return jsonify({"success": True, "chat": chat_result["result"], "member_count": member_count})

# Required for Vercel
# Disable debug mode as it causes issues in serverless environments
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

