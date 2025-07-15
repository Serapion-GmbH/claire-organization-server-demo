#!/bin/bash

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}   Claire API Key Generator${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
}

# Function to validate URL format
validate_url() {
    local url=$1
    if [[ $url =~ ^https?:// ]]; then
        return 0
    else
        return 1
    fi
}

# Function to validate organization ID format
validate_org_id() {
    local org_id=$1
    if [[ $org_id =~ ^org-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to validate JWT token format (basic check)
validate_jwt() {
    local jwt=$1
    if [[ $jwt =~ ^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# Main script
main() {
    print_header
    
    print_info "This script will help you generate an API key for your organization in the Claire system."
    print_info "You'll need to provide some information about your organization and authentication."
    echo
    
    # Set fixed base URL
    base_url="https://api-core.nova-ai.de"
    print_info "📍 Using Claire API at: $base_url"
    echo
    
    # Get organization ID
    print_info "🏢 Organization ID Information:"
    echo "   The organization ID is a unique identifier for your organization in Claire."
    echo "   Format: org-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    echo "   Example: org-86e4f084-c003-4b92-84d0-58ea82a512da"
    echo
    while true; do
        read -p "Enter your organization ID: " org_id
        
        if [[ -z "$org_id" ]]; then
            print_error "Organization ID cannot be empty."
            continue
        fi
        
        if validate_org_id "$org_id"; then
            break
        else
            print_error "Invalid organization ID format. Expected format: org-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        fi
    done
    
    # Get authorization token
    print_info "🔐 Authorization Token Information:"
    echo "   The authorization token is a JWT (JSON Web Token) used to authenticate your request."
    echo "   You can obtain this token by logging into your Claire account through Auth0."
    echo "   Format: Bearer <jwt_token>"
    echo "   Example: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
    echo
    while true; do
        read -p "Enter your authorization token (JWT): " auth_token
        
        if [[ -z "$auth_token" ]]; then
            print_error "Authorization token cannot be empty."
            continue
        fi
        
        # Remove "Bearer " prefix if present
        auth_token=${auth_token#"Bearer "}
        
        if validate_jwt "$auth_token"; then
            break
        else
            print_error "Invalid JWT format. Please enter a valid JWT token."
        fi
    done
    
    # Get API key label
    print_info "🏷️  API Key Label Information:"
    echo "   The label is a human-readable name for your API key to help you identify it later."
    echo "   Choose a descriptive name that helps you remember what this key is used for."
    echo "   Example: 'Production API Key', 'Development Key', 'Organization Server Demo'"
    echo
    read -p "Enter a label for your API key (default: 'Organization Server Demo'): " api_key_label
    api_key_label=${api_key_label:-"Organization Server Demo"}
    
    # Get expiration date
    print_info "📅 Expiration Date Information:"
    echo "   Set when this API key should expire for security purposes."
    echo "   Format: YYYY-MM-DDTHH:MM:SS.sssZ (ISO 8601)"
    echo "   Example: 2025-12-31T23:59:59.000Z"
    echo
    read -p "Enter expiration date (default: 2025-12-31T23:59:59.000Z): " expires_at
    expires_at=${expires_at:-"2025-12-31T23:59:59.000Z"}
    
    # Confirm details
    echo
    print_info "📋 Summary of your API key request:"
    echo "   Base URL: $base_url"
    echo "   Organization ID: $org_id"
    echo "   API Key Label: $api_key_label"
    echo "   Expires At: $expires_at"
    echo "   Authorization: Bearer ${auth_token:0:20}..."
    echo
    
    read -p "Do you want to proceed with creating the API key? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_warning "Operation cancelled."
        exit 0
    fi
    
    # Build the curl command
    endpoint="$base_url/organizations/$org_id/api_keys"
    
    print_info "🚀 Creating API key..."
    echo
    
    # Execute the curl command
    response=$(curl -s -w "\n%{http_code}" -X 'POST' \
        "$endpoint" \
        -H 'accept: application/json' \
        -H "Authorization: Bearer $auth_token" \
        -H 'Content-Type: application/json' \
        -d "{
            \"label\": \"$api_key_label\",
            \"scopes\": [\"session\"],
            \"expires_at\": \"$expires_at\"
        }")
    
    # Parse response
    http_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]] || [[ "$http_code" == "201" ]]; then
        print_success "API key created successfully!"
        echo
        
        # Extract the secret (API key) from the response
        api_key=$(echo "$response_body" | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    print(data['secret'])
except:
    sys.exit(1)
" 2>/dev/null)
        
        if [[ -n "$api_key" ]]; then
            print_info "Your API key:"
            echo "$api_key"
            echo
            print_info "💡 Next steps:"
            echo "  1. Copy the API key above"
            echo "  2. Add it to your .env.local file as "
            echo "  CLAIRE__API_KEY=\"$api_key\""
            echo "  3. Keep the API key secure and don't share it publicly"
        else
            print_warning "Could not extract API key from response. Full response:"
            echo "$response_body" | python3 -m json.tool 2>/dev/null || echo "$response_body"
        fi
    else
        print_error "Failed to create API key. HTTP Status: $http_code"
        echo
        print_info "Response:"
        echo "$response_body" | python3 -m json.tool 2>/dev/null || echo "$response_body"
        echo
        print_info "💡 Troubleshooting tips:"
        echo "   • Check if your organization ID is correct"
        echo "   • Verify your authorization token is valid and not expired"
        echo "   • Ensure you have permission to create API keys for this organization"
        echo "   • Check if the Claire API server is running and accessible"
    fi
}

# Run the main function
main "$@"