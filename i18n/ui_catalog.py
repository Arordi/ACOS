from __future__ import annotations

from typing import Any


# ============================================================
# ACOS UI LANGUAGE CATALOG
# ============================================================
#
# Default / primary language:
#   English (en)
#
# Supported languages:
#   hy  Armenian
#   en  English
#   ru  Russian
#   zh  Chinese
#   hi  Hindi
#   es  Spanish
#   ar  Arabic
#   fr  French
#   bn  Bengali
#   pt  Portuguese
#   id  Indonesian
#   ur  Urdu
#   de  German
#   ja  Japanese
#   pcm Nigerian Pidgin
#
# ============================================================


DEFAULT_LANGUAGE = "en"


SUPPORTED_LANGUAGES: tuple[str, ...] = (
    "hy",
    "en",
    "ru",
    "zh",
    "hi",
    "es",
    "ar",
    "fr",
    "bn",
    "pt",
    "id",
    "ur",
    "de",
    "ja",
    "pcm",
)


# ============================================================
# UI CATALOG
# ============================================================

UI_CATALOG: dict[str, dict[str, Any]] = {

    # --------------------------------------------------------
    # ARMENIAN
    # --------------------------------------------------------
    "hy": {
        "code": "hy",
        "name": "Հայերեն",
        "native_name": "Հայերեն",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "AI կինոստուդիա",

        "menu_home": "Գլխավոր",
        "menu_projects": "Նախագծեր",
        "menu_create": "Ստեղծել",
        "menu_media": "Մեդիա",
        "menu_settings": "Կարգավորումներ",
        "menu_language": "Լեզու",

        "new_project": "Նոր նախագիծ",
        "create_project": "Ստեղծել նախագիծ",
        "project_name": "Նախագծի անուն",
        "project_description": "Նկարագրություն",
        "project_type": "Տեսակ",

        "idea": "Գաղափար",
        "script": "Սցենար",
        "characters": "Կերպարներ",
        "storyboard": "Storyboard",
        "scenes": "Տեսարաններ",
        "video": "Տեսանյութ",
        "voice": "Ձայն",
        "music": "Երաժշտություն",
        "translation": "Թարգմանություն",
        "dubbing": "Դուբլյաժ",
        "subtitles": "Ենթագրեր",
        "render": "Render",
        "final_video": "Վերջնական տեսանյութ",

        "generate": "Ստեղծել",
        "generate_video": "Ստեղծել տեսանյութ",
        "upload": "Վերբեռնել",
        "download": "Ներբեռնել",
        "save": "Պահպանել",
        "cancel": "Չեղարկել",
        "delete": "Ջնջել",
        "edit": "Խմբագրել",
        "back": "Հետ",
        "next": "Հաջորդ",
        "previous": "Նախորդ",

        "loading": "Բեռնվում է...",
        "processing": "Մշակվում է...",
        "success": "Հաջողությամբ ավարտվեց",
        "error": "Սխալ",
        "not_found": "Չգտնվեց",

        "no_projects": "Նախագծեր դեռ չկան",
        "project_created": "Նախագիծը ստեղծվեց",
        "project_deleted": "Նախագիծը ջնջվեց",
    },

    # --------------------------------------------------------
    # ENGLISH — DEFAULT
    # --------------------------------------------------------
    "en": {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "AI Film Studio",

        "menu_home": "Home",
        "menu_projects": "Projects",
        "menu_create": "Create",
        "menu_media": "Media",
        "menu_settings": "Settings",
        "menu_language": "Language",

        "new_project": "New Project",
        "create_project": "Create Project",
        "project_name": "Project Name",
        "project_description": "Description",
        "project_type": "Type",

        "idea": "Idea",
        "script": "Script",
        "characters": "Characters",
        "storyboard": "Storyboard",
        "scenes": "Scenes",
        "video": "Video",
        "voice": "Voice",
        "music": "Music",
        "translation": "Translation",
        "dubbing": "Dubbing",
        "subtitles": "Subtitles",
        "render": "Render",
        "final_video": "Final Video",

        "generate": "Generate",
        "generate_video": "Generate Video",
        "upload": "Upload",
        "download": "Download",
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "edit": "Edit",
        "back": "Back",
        "next": "Next",
        "previous": "Previous",

        "loading": "Loading...",
        "processing": "Processing...",
        "success": "Completed successfully",
        "error": "Error",
        "not_found": "Not found",

        "no_projects": "No projects yet",
        "project_created": "Project created",
        "project_deleted": "Project deleted",
    },

    # --------------------------------------------------------
    # RUSSIAN
    # --------------------------------------------------------
    "ru": {
        "code": "ru",
        "name": "Russian",
        "native_name": "Русский",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "AI киностудия",

        "menu_home": "Главная",
        "menu_projects": "Проекты",
        "menu_create": "Создать",
        "menu_media": "Медиа",
        "menu_settings": "Настройки",
        "menu_language": "Язык",

        "new_project": "Новый проект",
        "create_project": "Создать проект",
        "project_name": "Название проекта",
        "project_description": "Описание",
        "project_type": "Тип",

        "idea": "Идея",
        "script": "Сценарий",
        "characters": "Персонажи",
        "storyboard": "Раскадровка",
        "scenes": "Сцены",
        "video": "Видео",
        "voice": "Голос",
        "music": "Музыка",
        "translation": "Перевод",
        "dubbing": "Дубляж",
        "subtitles": "Субтитры",
        "render": "Рендер",
        "final_video": "Финальное видео",

        "generate": "Создать",
        "generate_video": "Создать видео",
        "upload": "Загрузить",
        "download": "Скачать",
        "save": "Сохранить",
        "cancel": "Отмена",
        "delete": "Удалить",
        "edit": "Изменить",
        "back": "Назад",
        "next": "Далее",
        "previous": "Назад",

        "loading": "Загрузка...",
        "processing": "Обработка...",
        "success": "Успешно завершено",
        "error": "Ошибка",
        "not_found": "Не найдено",

        "no_projects": "Проектов пока нет",
        "project_created": "Проект создан",
        "project_deleted": "Проект удалён",
    },

    # --------------------------------------------------------
    # CHINESE
    # --------------------------------------------------------
    "zh": {
        "code": "zh",
        "name": "Chinese",
        "native_name": "中文",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "AI 电影工作室",

        "menu_home": "首页",
        "menu_projects": "项目",
        "menu_create": "创建",
        "menu_media": "媒体",
        "menu_settings": "设置",
        "menu_language": "语言",

        "new_project": "新项目",
        "create_project": "创建项目",
        "project_name": "项目名称",
        "project_description": "描述",
        "project_type": "类型",

        "idea": "创意",
        "script": "剧本",
        "characters": "角色",
        "storyboard": "分镜",
        "scenes": "场景",
        "video": "视频",
        "voice": "声音",
        "music": "音乐",
        "translation": "翻译",
        "dubbing": "配音",
        "subtitles": "字幕",
        "render": "渲染",
        "final_video": "最终视频",

        "generate": "生成",
        "generate_video": "生成视频",
        "upload": "上传",
        "download": "下载",
        "save": "保存",
        "cancel": "取消",
        "delete": "删除",
        "edit": "编辑",
        "back": "返回",
        "next": "下一步",
        "previous": "上一步",

        "loading": "加载中...",
        "processing": "处理中...",
        "success": "成功完成",
        "error": "错误",
        "not_found": "未找到",

        "no_projects": "暂无项目",
        "project_created": "项目已创建",
        "project_deleted": "项目已删除",
    },

    # --------------------------------------------------------
    # HINDI
    # --------------------------------------------------------
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native_name": "हिन्दी",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "AI फिल्म स्टूडियो",

        "menu_home": "होम",
        "menu_projects": "प्रोजेक्ट",
        "menu_create": "बनाएं",
        "menu_media": "मीडिया",
        "menu_settings": "सेटिंग्स",
        "menu_language": "भाषा",

        "new_project": "नया प्रोजेक्ट",
        "create_project": "प्रोजेक्ट बनाएं",
        "project_name": "प्रोजेक्ट का नाम",
        "project_description": "विवरण",
        "project_type": "प्रकार",

        "idea": "विचार",
        "script": "स्क्रिप्ट",
        "characters": "पात्र",
        "storyboard": "स्टोरीबोर्ड",
        "scenes": "दृश्य",
        "video": "वीडियो",
        "voice": "आवाज़",
        "music": "संगीत",
        "translation": "अनुवाद",
        "dubbing": "डबिंग",
        "subtitles": "उपशीर्षक",
        "render": "रेंडर",
        "final_video": "अंतिम वीडियो",

        "generate": "बनाएं",
        "generate_video": "वीडियो बनाएं",
        "upload": "अपलोड",
        "download": "डाउनलोड",
        "save": "सहेजें",
        "cancel": "रद्द करें",
        "delete": "हटाएं",
        "edit": "संपादित करें",
        "back": "वापस",
        "next": "अगला",
        "previous": "पिछला",

        "loading": "लोड हो रहा है...",
        "processing": "प्रक्रिया जारी है...",
        "success": "सफलतापूर्वक पूरा हुआ",
        "error": "त्रुटि",
        "not_found": "नहीं मिला",

        "no_projects": "अभी कोई प्रोजेक्ट नहीं है",
        "project_created": "प्रोजेक्ट बनाया गया",
        "project_deleted": "प्रोजेक्ट हटा दिया गया",
    },

    # --------------------------------------------------------
    # SPANISH
    # --------------------------------------------------------
    "es": {
        "code": "es",
        "name": "Spanish",
        "native_name": "Español",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "Estudio de Cine con IA",

        "menu_home": "Inicio",
        "menu_projects": "Proyectos",
        "menu_create": "Crear",
        "menu_media": "Medios",
        "menu_settings": "Configuración",
        "menu_language": "Idioma",

        "new_project": "Nuevo proyecto",
        "create_project": "Crear proyecto",
        "project_name": "Nombre del proyecto",
        "project_description": "Descripción",
        "project_type": "Tipo",

        "idea": "Idea",
        "script": "Guion",
        "characters": "Personajes",
        "storyboard": "Storyboard",
        "scenes": "Escenas",
        "video": "Vídeo",
        "voice": "Voz",
        "music": "Música",
        "translation": "Traducción",
        "dubbing": "Doblaje",
        "subtitles": "Subtítulos",
        "render": "Renderizado",
        "final_video": "Vídeo final",

        "generate": "Generar",
        "generate_video": "Generar vídeo",
        "upload": "Subir",
        "download": "Descargar",
        "save": "Guardar",
        "cancel": "Cancelar",
        "delete": "Eliminar",
        "edit": "Editar",
        "back": "Atrás",
        "next": "Siguiente",
        "previous": "Anterior",

        "loading": "Cargando...",
        "processing": "Procesando...",
        "success": "Completado correctamente",
        "error": "Error",
        "not_found": "No encontrado",

        "no_projects": "Aún no hay proyectos",
        "project_created": "Proyecto creado",
        "project_deleted": "Proyecto eliminado",
    },

    # --------------------------------------------------------
    # ARABIC
    # --------------------------------------------------------
    "ar": {
        "code": "ar",
        "name": "Arabic",
        "native_name": "العربية",
        "direction": "rtl",

        "app_name": "ACOS",
        "app_subtitle": "استوديو أفلام بالذكاء الاصطناعي",

        "menu_home": "الرئيسية",
        "menu_projects": "المشاريع",
        "menu_create": "إنشاء",
        "menu_media": "الوسائط",
        "menu_settings": "الإعدادات",
        "menu_language": "اللغة",

        "new_project": "مشروع جديد",
        "create_project": "إنشاء مشروع",
        "project_name": "اسم المشروع",
        "project_description": "الوصف",
        "project_type": "النوع",

        "idea": "الفكرة",
        "script": "السيناريو",
        "characters": "الشخصيات",
        "storyboard": "لوحة القصة",
        "scenes": "المشاهد",
        "video": "الفيديو",
        "voice": "الصوت",
        "music": "الموسيقى",
        "translation": "الترجمة",
        "dubbing": "الدبلجة",
        "subtitles": "الترجمة النصية",
        "render": "التصيير",
        "final_video": "الفيديو النهائي",

        "generate": "إنشاء",
        "generate_video": "إنشاء فيديو",
        "upload": "رفع",
        "download": "تنزيل",
        "save": "حفظ",
        "cancel": "إلغاء",
        "delete": "حذف",
        "edit": "تعديل",
        "back": "رجوع",
        "next": "التالي",
        "previous": "السابق",

        "loading": "جارٍ التحميل...",
        "processing": "جارٍ المعالجة...",
        "success": "اكتمل بنجاح",
        "error": "خطأ",
        "not_found": "غير موجود",

        "no_projects": "لا توجد مشاريع بعد",
        "project_created": "تم إنشاء المشروع",
        "project_deleted": "تم حذف المشروع",
    },

    # --------------------------------------------------------
    # FRENCH
    # --------------------------------------------------------
    "fr": {
        "code": "fr",
        "name": "French",
        "native_name": "Français",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "Studio de cinéma IA",

        "menu_home": "Accueil",
        "menu_projects": "Projets",
        "menu_create": "Créer",
        "menu_media": "Médias",
        "menu_settings": "Paramètres",
        "menu_language": "Langue",

        "new_project": "Nouveau projet",
        "create_project": "Créer un projet",
        "project_name": "Nom du projet",
        "project_description": "Description",
        "project_type": "Type",

        "idea": "Idée",
        "script": "Scénario",
        "characters": "Personnages",
        "storyboard": "Storyboard",
        "scenes": "Scènes",
        "video": "Vidéo",
        "voice": "Voix",
        "music": "Musique",
        "translation": "Traduction",
        "dubbing": "Doublage",
        "subtitles": "Sous-titres",
        "render": "Rendu",
        "final_video": "Vidéo finale",

        "generate": "Générer",
        "generate_video": "Générer une vidéo",
        "upload": "Téléverser",
        "download": "Télécharger",
        "save": "Enregistrer",
        "cancel": "Annuler",
        "delete": "Supprimer",
        "edit": "Modifier",
        "back": "Retour",
        "next": "Suivant",
        "previous": "Précédent",

        "loading": "Chargement...",
        "processing": "Traitement...",
        "success": "Terminé avec succès",
        "error": "Erreur",
        "not_found": "Introuvable",

        "no_projects": "Aucun projet pour le moment",
        "project_created": "Projet créé",
        "project_deleted": "Projet supprimé",
    },

    # --------------------------------------------------------
    # BENGALI
    # --------------------------------------------------------
    "bn": {
        "code": "bn",
        "name": "Bengali",
        "native_name": "বাংলা",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "AI ফিল্ম স্টুডিও",

        "menu_home": "হোম",
        "menu_projects": "প্রকল্প",
        "menu_create": "তৈরি করুন",
        "menu_media": "মিডিয়া",
        "menu_settings": "সেটিংস",
        "menu_language": "ভাষা",

        "new_project": "নতুন প্রকল্প",
        "create_project": "প্রকল্প তৈরি করুন",
        "project_name": "প্রকল্পের নাম",
        "project_description": "বিবরণ",
        "project_type": "ধরন",

        "idea": "ধারণা",
        "script": "চিত্রনাট্য",
        "characters": "চরিত্র",
        "storyboard": "স্টোরিবোর্ড",
        "scenes": "দৃশ্য",
        "video": "ভিডিও",
        "voice": "কণ্ঠ",
        "music": "সঙ্গীত",
        "translation": "অনুবাদ",
        "dubbing": "ডাবিং",
        "subtitles": "সাবটাইটেল",
        "render": "রেন্ডার",
        "final_video": "চূড়ান্ত ভিডিও",

        "generate": "তৈরি করুন",
        "generate_video": "ভিডিও তৈরি করুন",
        "upload": "আপলোড",
        "download": "ডাউনলোড",
        "save": "সংরক্ষণ",
        "cancel": "বাতিল",
        "delete": "মুছুন",
        "edit": "সম্পাদনা",
        "back": "পিছনে",
        "next": "পরবর্তী",
        "previous": "পূর্ববর্তী",

        "loading": "লোড হচ্ছে...",
        "processing": "প্রক্রিয়াকরণ চলছে...",
        "success": "সফলভাবে সম্পন্ন হয়েছে",
        "error": "ত্রুটি",
        "not_found": "পাওয়া যায়নি",

        "no_projects": "এখনও কোনো প্রকল্প নেই",
        "project_created": "প্রকল্প তৈরি হয়েছে",
        "project_deleted": "প্রকল্প মুছে ফেলা হয়েছে",
    },

    # --------------------------------------------------------
    # PORTUGUESE
    # --------------------------------------------------------
    "pt": {
        "code": "pt",
        "name": "Portuguese",
        "native_name": "Português",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "Estúdio de Cinema com IA",

        "menu_home": "Início",
        "menu_projects": "Projetos",
        "menu_create": "Criar",
        "menu_media": "Mídia",
        "menu_settings": "Configurações",
        "menu_language": "Idioma",

        "new_project": "Novo projeto",
        "create_project": "Criar projeto",
        "project_name": "Nome do projeto",
        "project_description": "Descrição",
        "project_type": "Tipo",

        "idea": "Ideia",
        "script": "Roteiro",
        "characters": "Personagens",
        "storyboard": "Storyboard",
        "scenes": "Cenas",
        "video": "Vídeo",
        "voice": "Voz",
        "music": "Música",
        "translation": "Tradução",
        "dubbing": "Dublagem",
        "subtitles": "Legendas",
        "render": "Renderização",
        "final_video": "Vídeo final",

        "generate": "Gerar",
        "generate_video": "Gerar vídeo",
        "upload": "Enviar",
        "download": "Baixar",
        "save": "Salvar",
        "cancel": "Cancelar",
        "delete": "Excluir",
        "edit": "Editar",
        "back": "Voltar",
        "next": "Próximo",
        "previous": "Anterior",

        "loading": "Carregando...",
        "processing": "Processando...",
        "success": "Concluído com sucesso",
        "error": "Erro",
        "not_found": "Não encontrado",

        "no_projects": "Ainda não há projetos",
        "project_created": "Projeto criado",
        "project_deleted": "Projeto excluído",
    },

    # --------------------------------------------------------
    # INDONESIAN
    # --------------------------------------------------------
    "id": {
        "code": "id",
        "name": "Indonesian",
        "native_name": "Bahasa Indonesia",
        "direction": "ltr",

        "app_name": "ACOS",
        "app_subtitle": "Studio Film AI",

        "menu_home": "Beranda",
        "menu_projects": "Proyek",
        "menu_create": "Buat",
        "menu_media": "Media",
        "menu_settings": "Pengaturan",
        "menu_language": "Bahasa",

        "new_project": "Proyek Baru",
        "create_project": "Buat Proyek",
        "project_name": "Nama Proyek",
        "project_description": "Deskripsi",
        "project_type": "Jenis",

        "idea": "Ide",
        "script": "Naskah",
        "characters": "Karakter",
        "storyboard": "Storyboard",
        "scenes": "Adegan",
        "video": "Video",
        "voice": "Suara",
        "music": "Musik",
        "translation": "Terjemahan",
        "dubbing": "Sulih Suara",
        "subtitles": "Subtitle",
        "render": "Render",
        "final_video": "Video Ak
