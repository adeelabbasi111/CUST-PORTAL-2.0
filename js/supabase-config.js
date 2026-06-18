// Supabase Configuration
const SUPABASE_URL = 'https://wrhuwxshniygeniphfnt.supabase.co'; // Apna URL yahan dalein
const SUPABASE_ANON_KEY = "sb_publishable_otNkoOXheD7Y9yLGiexsoQ_ZFEBw0e5"; // Apni anon key yahan dalein

// Initialize Supabase client - NAYA NAAM: supabaseClient
const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

console.log('✅ Supabase connected successfully');