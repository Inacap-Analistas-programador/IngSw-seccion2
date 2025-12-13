import { request } from './apiClient'

export default {
    /**
     * Send an email to a list of recipients.
     * @param {object} payload - { recipient_ids: [], subject: '', message: '', curso_id: (optional) }
     */
    sendEmail: (payload) => request('correos/correos/send/', {
        method: 'POST',
        body: JSON.stringify(payload)
    })
}
