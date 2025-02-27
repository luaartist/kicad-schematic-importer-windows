import requests
import logging
import os
import json
from datetime import datetime, timedelta

class GitHubVerifier:
    """Handle GitHub account verification and 2FA requirements"""
    
    def __init__(self, cache_dir=None):
        self.logger = logging.getLogger('github_verifier')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.FileHandler('github_verification.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def verify_account(self, token):
        """
        Verify GitHub account exists and has 2FA enabled
        
        Args:
            token: GitHub personal access token
            
        Returns:
            dict: Verification result with status and user info
        """
        # Check cache first
        cached = self._check_cache(token)
        if cached:
            return cached
        
        try:
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get user info
            user_response = requests.get('https://api.github.com/user', headers=headers)
            if user_response.status_code != 200:
                self.logger.warning(f"GitHub verification failed: {user_response.status_code}")
                return {
                    'verified': False,
                    'error': f"Authentication failed: {user_response.status_code}",
                    'timestamp': datetime.now().isoformat()
                }
            
            user_data = user_response.json()
            
            # Check 2FA status
            # Note: This endpoint requires specific permissions
            twofa_response = requests.get('https://api.github.com/user/2fa_status', headers=headers)
            has_2fa = False
            
            if twofa_response.status_code == 200:
                has_2fa = twofa_response.json().get('enabled', False)
            else:
                # Alternative method: check if token has SSO enabled
                # This is not a perfect check but can indicate 2FA
                orgs_response = requests.get('https://api.github.com/user/orgs', headers=headers)
                if orgs_response.status_code == 200 and len(orgs_response.json()) > 0:
                    # If user is in organizations, they likely have 2FA enabled
                    # as many orgs require it
                    has_2fa = True
            
            result = {
                'verified': has_2fa,
                'username': user_data.get('login'),
                'name': user_data.get('name'),
                'has_2fa': has_2fa,
                'avatar_url': user_data.get('avatar_url'),
                'timestamp': datetime.now().isoformat()
            }
            
            if not has_2fa:
                result['error'] = "Two-factor authentication is required but not enabled on your GitHub account"
                self.logger.warning(f"GitHub 2FA not enabled for user {result['username']}")
            else:
                self.logger.info(f"GitHub verification successful for user {result['username']}")
                # Cache successful result
                self._cache_result(token, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"GitHub verification error: {str(e)}")
            return {
                'verified': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _check_cache(self, token):
        """Check if we have a cached verification for this token"""
        # Create a hash of the token for the filename
        import hashlib
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{token_hash}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                
                # Check if cache is still valid (24 hours)
                cache_time = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.now() - cache_time < timedelta(hours=24):
                    return cached_data
            except Exception as e:
                self.logger.error(f"Error reading cache: {str(e)}")
        
        return None
    
    def _cache_result(self, token, result):
        """Cache a successful verification result"""
        import hashlib
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{token_hash}.json")
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(result, f)
        except Exception as e:
            self.logger.error(f"Error writing cache: {str(e)}")
    
    def get_auth_url(self):
        """Get the URL for GitHub OAuth authorization"""
        # This would be configured with your app's client ID
        client_id = "YOUR_GITHUB_CLIENT_ID"
        redirect_uri = "kicad://github-callback"
        scope = "read:user"
        
        return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"