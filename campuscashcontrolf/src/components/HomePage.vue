<template>
	<el-container class="home-root">
		<el-main class="home-main">
			<section
				:class="['hero-panel', { 'is-dark': isDarkMode }]"
				@mousemove="handleHeroPointerMove"
				@mouseleave="resetHeroPointer"
			>
				<HeroDotBackground ref="dotBackground" :is-dark-mode="isDarkMode" />

				<HomeNavBar
					:is-dark-mode="isDarkMode"
					:mobile-menu-open="mobileMenuOpen"
					@update:isDarkMode="isDarkMode = $event"
					@update:mobileMenuOpen="mobileMenuOpen = $event"
					@navigate="navigate"
					@open-login="openLoginModal"
				/>

				<div class="hero-overlay">
					<h1>CampusCashControl</h1>
					<p>Manage and monitor university financial activity with clarity.</p>
				</div>

				<HomeFooter
					:is-dark-mode="isDarkMode"
					:current-year="currentYear"
					:footer-links="footerLinks"
					@link-click="handleFooterLink"
				/>

				<el-dialog
					v-model="loginDialogOpen"
					:show-header="false"
					width="420px"
					append-to-body
					:modal-class="isDarkMode ? 'login-dialog-modal is-dark' : 'login-dialog-modal'"
					:class="['login-dialog', { 'is-dark': isDarkMode }]"
				>
					<LoginForm :is-dark="isDarkMode" />
				</el-dialog>
			</section>
		</el-main>
	</el-container>
</template>

<script>
import { ElNotification } from "element-plus";
import LoginForm from "@/components/LoginForm.vue";
import HeroDotBackground from "@/components/home/HeroDotBackground.vue";
import HomeNavBar from "@/components/home/HomeNavBar.vue";
import HomeFooter from "@/components/home/HomeFooter.vue";
import { setDarkMode, themeState } from "@/state/themeState";

export default {
	name: "HomePage",
	components: {
		LoginForm,
		HeroDotBackground,
		HomeNavBar,
		HomeFooter,
	},
	data() {
		return {
			mobileMenuOpen: false,
			loginDialogOpen: false,
			footerLinks: [
				{ title: "Features" },
				{ title: "Dashboard", path: "/dashboard" },
				{ title: "Departments", path: "/departments" },
				{ title: "Upload", path: "/upload" },
				{ title: "Reports", path: "/reports" },
				{ title: "User Access", path: "/useraccess" },
			],
		};
	},
	computed: {
		isDarkMode: {
			get() {
				return themeState.isDarkMode;
			},
			set(value) {
				setDarkMode(value);
			},
		},
		currentYear() {
			return new Date().getFullYear();
		},
	},
	methods: {
		isAuthenticated() {
			return !!(sessionStorage.getItem("access_token") || localStorage.getItem("access_token"));
		},
		navigate(path) {
			if (!this.isAuthenticated()) {
				ElNotification({
					title: "Sign in required",
					message: "Please login first to access this page.",
					type: "warning",
				});
				this.mobileMenuOpen = false;
				return;
			}

			this.mobileMenuOpen = false;
			this.$router.push(path);
		},
		openLoginModal() {
			this.mobileMenuOpen = false;
			this.loginDialogOpen = true;
		},
		handleFooterLink(link) {
			if (!link.path) {
				return;
			}
			this.navigate(link.path);
		},
		handleHeroPointerMove(event) {
			this.$refs.dotBackground?.onPointerMove?.(event);
		},
		resetHeroPointer() {
			this.$refs.dotBackground?.onPointerLeave?.();
		},
	},
};
</script>

<style scoped>
.home-root {
	min-height: 100vh;
}

.home-main {
	display: block;
	min-height: 100vh;
	padding: 0;
}

.hero-panel {
	--panel-bg: #ffffff;
	--footer-space: 118px;
	background: #ffffff;
	position: relative;
	min-height: 100vh;
	overflow: hidden;
}

.hero-panel.is-dark {
	--panel-bg: #0b0f14;
	background: #0b0f14;
}

.dot-background {
	position: absolute;
	inset: 0;
	z-index: 1;
	pointer-events: none;
	background-color: var(--panel-bg);
	transition: background-color 220ms ease;
}

.dot-canvas {
	position: absolute;
	inset: 0;
	width: 100%;
	height: 100%;
	display: block;
}

.floating-nav {
	position: absolute;
	top: 16px;
	left: 50%;
	transform: translateX(-50%);
	width: min(1040px, calc(100% - 36px));
	z-index: 30;
	border: 1px solid rgba(255, 255, 255, 0.48);
	background: rgba(255, 255, 255, 0.12);
	backdrop-filter: blur(10px);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.hero-panel.is-dark .floating-nav {
	border: 1px solid rgba(164, 181, 203, 0.35);
	background: rgba(8, 12, 19, 0.62);
	box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
}

.floating-nav :deep(.el-card__body) {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 14px;
	padding: 6px 12px;
	flex-wrap: nowrap;
}

.brand-wrap {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	font-weight: 800;
	color: #212121;
	white-space: nowrap;
	font-size: 1rem;
	flex: 0 0 auto;
}

.hero-panel.is-dark .brand-wrap {
	color: #edf2fb;
}

.hero-links {
	flex: 1;
	min-width: 0;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	overflow: visible;
}

.hero-link-btn {
	height: 32px;
	padding: 0 8px;
	font-size: 0.9rem;
	font-weight: 600;
	color: #212121;
	display: inline-flex;
	align-items: center;
	gap: 6px;
	border-radius: 8px;
	white-space: nowrap;
	flex: 0 0 auto;
}

.hero-link-btn:hover {
	color: #f26d21;
	background: rgba(242, 109, 33, 0.08);
}

.hero-panel.is-dark .hero-link-btn {
	color: #d8e2f1;
}

.hero-panel.is-dark .hero-link-btn:hover {
	color: #ffb26e;
	background: rgba(255, 178, 110, 0.12);
}

.nav-actions {
	display: inline-flex;
	align-items: center;
	gap: 10px;
	flex: 0 0 auto;
}

.theme-toggle {
	--el-switch-on-color: #111a28;
	--el-switch-off-color: #e7edf5;
	--el-switch-border-color: rgba(20, 27, 38, 0.36);
}

.hero-panel.is-dark .theme-toggle {
	--el-switch-on-color: #f5f8ff;
	--el-switch-off-color: #55657d;
	--el-switch-border-color: rgba(220, 232, 247, 0.4);
}

.theme-toggle :deep(.el-switch__core) {
	border-width: 1px;
	box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.theme-toggle :deep(.el-switch__action) {
	color: #1c2532;
}

.hero-panel.is-dark .theme-toggle :deep(.el-switch__action) {
	color: #0f1724;
}

.mobile-nav-toggle {
	display: none;
}

.login-avatar-btn {
	width: 34px;
	height: 34px;
	min-width: 34px;
	max-width: 34px;
	padding: 0 !important;
	border-radius: 999px;
	background: rgba(18, 18, 18, 0.9);
	border: 1px solid rgba(18, 18, 18, 0.95);
	color: #ffffff;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	aspect-ratio: 1 / 1;
	flex: 0 0 34px;
}

.login-avatar-btn:hover {
	background: #242424;
	border-color: #242424;
	color: #ffffff;
}

.hero-panel.is-dark .login-avatar-btn {
	background: rgba(241, 246, 255, 0.95);
	border-color: rgba(241, 246, 255, 0.95);
	color: #111826;
}

.hero-panel.is-dark .login-avatar-btn:hover {
	background: #ffffff;
	border-color: #ffffff;
	color: #111826;
}

.mobile-nav-list {
	display: grid;
	gap: 8px;
}

.mobile-nav-list .el-button {
	justify-content: flex-start;
}

.hero-overlay {
	position: absolute;
	inset: 0 0 var(--footer-space) 0;
	z-index: 10;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
	color: #1d252e;
	background: linear-gradient(160deg, rgba(255, 255, 255, 0.64), rgba(250, 251, 252, 0.78));
	padding: 48px;
}

.hero-panel.is-dark .hero-overlay {
	color: #eef3ff;
	background: linear-gradient(160deg, rgba(11, 15, 24, 0.55), rgba(11, 15, 24, 0.72));
}

.hero-overlay h1 {
	margin: 0 0 12px;
	font-size: 3rem;
	font-weight: 800;
	text-shadow: 0 1px 0 rgba(255, 255, 255, 0.65);
}

.hero-overlay p {
	margin: 0;
	font-size: 1.1rem;
	max-width: 520px;
	color: #38424d;
}

.hero-panel.is-dark .hero-overlay h1 {
	text-shadow: 0 1px 0 rgba(0, 0, 0, 0.45);
}

.hero-panel.is-dark .hero-overlay p {
	color: #c3cfdf;
}

.hero-footer {
	position: absolute;
	left: 0;
	right: 0;
	bottom: 0;
	height: var(--footer-space);
	box-sizing: border-box;
	z-index: 12;
	padding: 14px 24px 18px;
	background: linear-gradient(160deg, rgba(255, 255, 255, 0.64), rgba(250, 251, 252, 0.78));
}

.hero-panel.is-dark .hero-footer {
	background: linear-gradient(160deg, rgba(11, 15, 24, 0.55), rgba(11, 15, 24, 0.72));
}

.footer-inner {
	max-width: 1060px;
	margin: 0 auto;
	padding: 12px 14px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 14px;
}

.footer-links {
	display: flex;
	align-items: center;
	gap: 2px;
	flex-wrap: wrap;
}

.footer-link-btn {
	font-size: 0.86rem;
	font-weight: 600;
	color: #273140;
	padding: 0 8px;
	height: 28px;
}

.footer-link-btn:hover {
	color: #f26d21;
	background: rgba(242, 109, 33, 0.08);
}

.hero-panel.is-dark .footer-link-btn {
	color: #d7e3f6;
}

.hero-panel.is-dark .footer-link-btn:hover {
	color: #ffb26e;
	background: rgba(255, 178, 110, 0.12);
}

.footer-copy {
	font-size: 0.82rem;
	font-weight: 500;
	color: #445061;
	white-space: nowrap;
}

.hero-panel.is-dark .footer-copy {
	color: #b8c6d8;
}

:global(.login-dialog-modal .el-dialog) {
	background: #ffffff !important;
	border: none !important;
	outline: none;
	box-shadow: 0 24px 56px rgba(8, 18, 33, 0.18);
	border-radius: 16px;
}

:global(.login-dialog-modal .el-dialog__body) {
	padding: 20px;
	background: transparent;
}

:global(.login-dialog-modal.is-dark .el-dialog) {
	background: #000000 !important;
	border: none !important;
	outline: none;
	box-shadow: 0 26px 60px rgba(0, 0, 0, 0.5);
}

@media (max-width: 960px) {
	.hero-panel {
		--footer-space: 146px;
		min-height: 100vh;
	}

	.hero-overlay {
		inset: 0 0 var(--footer-space) 0;
	}

	.hero-menu {
		display: none;
	}

	.login-avatar-btn {
		display: none;
	}

	.theme-toggle {
		display: none;
	}

	.hero-links {
		display: none;
	}

	.mobile-nav-toggle {
		display: inline-flex;
	}

	.floating-nav {
		left: 50%;
		transform: translateX(-50%);
		width: calc(100% - 20px);
		top: 10px;
	}

	.floating-nav :deep(.el-card__body) {
		padding: 6px 10px;
	}

	.hero-footer {
		padding: 10px 12px 14px;
	}

	.footer-inner {
		padding: 10px 8px;
		flex-direction: column;
		align-items: flex-start;
		gap: 8px;
	}

	.footer-links {
		gap: 0;
	}

	.footer-copy {
		font-size: 0.78rem;
	}
}
</style>
